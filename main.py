#! /bin/usr/python3.5
from flask import Flask, request, render_template, send_from_directory, redirect, session
from Crypto.Hash import SHA256
import sqlite3 as sqlite
import os

app            = Flask( __name__, static_folder = 'static', static_url_path = '' )
app.secret_key = Random.new( os.environ [ "SEED" ] ).read(16)

def connect():
    con = sqlite.connect( 'data.db' )
    cursor = con.cursor()
    return ( con, cursor )

@app.route ( "/" )
def index():
    if 'logged_in' in session and 'userId' in session:

        ( connection, cursor ) = connect()

        userId = session [ 'userId' ]
        # SELECT all contents from all people userId is following
        query_feed = """
SELECT * FROM contents WHERE author_id IN  ( SELECT follower FROM followers WHERE follower = ? )
        """
        cursor.execute( query_feed, [ userId ] )
        feed = cursor.fetchall()
        return render_template( 'feed.html', feed )
    else:
        return render_template( 'startpage.html' )

@app.route( "/id_to", methods=[ "POST" ] )
def info():
    ( connection, cursor )  = connect()

    types                   = {
        "name"      : "name"
    }

    type                    = type if types[ type ] else "ERROR"
    id                      = request.form[ 'id' ]
    query_feed              = "SELECT ? FROM users WHERE id = ?"
    cursor.execute( query_feed, type, id )
    answer                  = cursor.fetchone()
    return make_response( JSON.stringify( answer ) )
