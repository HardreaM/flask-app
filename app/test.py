import json
import psycopg2
import jwt

from flask import Flask, make_response, send_file
from flask import jsonify
from flask import render_template
from flask import request
from flask import redirect
from flask import make_response

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

"""
@app.route('/')
def hello():
    if not get_jwt_identity():
        access_token = create_access_token(identity='guest')
        return jsonify(get_jwt_identity())
    return jsonify(get_jwt_identity())"""

@app.route('/get_data')
def get_data():

    if request.method == 'POST':
        pass

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""SELECT * FROM "USERS";""")
    response = cur.fetchall()
    cur.close()
    conn.close()

    print(response)

    return jsonify(response)

@app.route('/test')
def test():

    """conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(""SELECT * FROM "USERS";"")
    response = cur.fetchall()
    cur.close()
    conn.close()"""
    
    return render_template('test.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.json.get('username')
        password = request.json.get('password')
        conn = get_db_connection()
        cur = conn.cursor()
        query = """SELECT * FROM "USERS" WHERE user_name=%s AND user_password=%s;"""
        cur.execute(query, (username, password))
        response = cur.fetchall()
        cur.close()
        conn.close()

        if len(response) == 0:

            return 400

        access_token = create_access_token(identity=username)
        
        return jsonify({"access_token": access_token, "success": True, "status": 200})
    
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

@app.route("/protected", methods=["GET", "POST"])
def protected():

    if request.method == 'POST':
        verify_jwt_in_request()
        token = request.headers['Authorization']
        #data = jwt.decode(token, app.config['SECRET_KEY'])
        print(get_jwt())
        if token:
            return jsonify(status="Success")
        return jsonify(status="Forbidden"), 403
    
    return render_template('protected.html')

@app.route("/view_table", methods=["GET"])
def view_table():
    return render_template('view_table.html')

@app.route("/redact_table", methods=["GET", "POST"])
def redact_table():

    if request.method == "POST":
        pass

    return render_template('redact_table.html')