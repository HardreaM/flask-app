import json
from flask import Flask, jsonify, render_template, request
import psycopg2

app = Flask(__name__)


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
        return jsonify(response)
    
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