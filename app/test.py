import json
import psycopg2

from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended import get_jwt
from flask_jwt_extended import set_access_cookies


app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "some-key"
jwt = JWTManager(app)

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='mydb',
                            user='myuser',
                            password='mypass')
    return conn


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/test')
def test():

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""SELECT * FROM "USERS";""")
    response = cur.fetchall()
    cur.close()
    conn.close()
    
    return render_template('base.html', data=response)

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')
        conn = get_db_connection()
        cur = conn.cursor()
        query = """SELECT * FROM "USERS" WHERE user_name=%s AND user_password=%s;"""
        cur.execute(query, (username, password))
        response = cur.fetchall()
        cur.close()
        conn.close()

        if len(response) == 0:

            return render_template('login.html', status='Wrong data, please try again')

        access_token = create_access_token(identity=username)
        response = jsonify({"msg": "login successful"})
        set_access_cookies(response, access_token)
        return render_template('login.html', status='Success')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')
        conn = get_db_connection()
        cur = conn.cursor()
        query = """SELECT * FROM "USERS" WHERE user_name=%s AND user_password=%s;"""
        cur.execute(query, (username, password))
        response = cur.fetchall()
        cur.close()
        conn.close()

        if len(response) == 0:
            conn = get_db_connection()
            cur = conn.cursor()
            query = """INSERT INTO "USERS" (user_name, user_password) VALUES (%s, %s)"""
            cur.execute(query, (username, password))
            conn.commit()
            cur.close()
            conn.close()
            return render_template('signup.html', status='Success')
            
        return render_template('signup.html', status='User already exists')

    return render_template('signup.html')

@app.route("/protected", methods=["GET"])
@jwt_required(optional=True)
def protected():
    current_user = get_jwt_identity()
    return jsonify(foo="bar")