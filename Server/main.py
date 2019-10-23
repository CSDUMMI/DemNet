from flask import Flask, request, session
from election import count_votes
from Crypto import SHA256
import sqlite3 as sqlite

app = Flask(__name__)

def connect():
    return sqlite.connect('data.db')

@app.route('/login')
def login():
    # Logout automatically
    if request.form.get('username') and request.form.get('password'):
        hash = SHA256.new( request.form.get('password') ).hexdigest()
        username = request.form.get('username')

        connection = connect()
        cursor = connection.cursor()
        cursor.execute('SELECT password FROM users WHERE username = ?', username )

        if hash == cursor.fetchone():
            session['username'] = username
            return 'ok'

        cursor.close()
    else:
        return 'fail'

@app.route('/register')
def register():

    if (
        request.form.get('username')
        and request.form.get('password')
        and request.form.get('email')
        ):

        username = request.form.get('username')
        hash = SHA256.new( request.form.get('password')).hexdigest()
        email = request.form.get('email')

        connection = connect()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO users VALUES ( ?, ?, ? )')
