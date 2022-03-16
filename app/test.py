import json
from flask import Flask, jsonify
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
    # cur.execute('SELECT * FROM information_schema.tables;')
    cur.execute("""SELECT * FROM "USERS";""")
    books = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(books)