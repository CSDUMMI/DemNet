#!/usr/bin/env python3

from Server import Elections, Patches, Users
from Server.Crypto import Storage
from flask import Flask, request, render_template
import pymongo
from pymongo import MongoClient
import json, os
from Crypto.Hash import SHA3_256

app = Flask( __name__
           , static_url_path="/static"
           , static_folder="output/static"
           , template_folder="output")
app.secret_key = os.environ["SECRET_KEY"]

# Errors
ok = 0
invalidData = 1
invalidContext = 2

@app.route("/", methods=["GET"])
def index():
    if session.get("username"):
        return render_template("index.html")
    else:
        return render_template("login.html")

@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")

@app.route("/readings", methods=["GET"])
def readings():
    if session.get("username"):
        client      = MongoClient()
        db          = client.demnet
        messages    = db.messages
        users       = db.users
        readings    = users.find_one({ "username" : session["username" ] })["readings"]
        readings    = [messages.find_one({ "hash" : reading }) for reading in readings]
        readings    = [{ key : reading[key] if key != "body" else Storage.encrypt(reading["body"]) for key in reading } for reading in readings]

        return render_template("readings-index.html", readings=readings)





@app.route("/login",methods=["POST"])
def login():
    username = request.values.get("username")
    password = request.values.get("password")

    if not session.get("keys") and username and password:
        sha3_256 = SHA3_256.new()
        sha3_256.update(password.encode('utf-8'))
        passphrase = sha3_256.hexdigest()
        keys = Users.login(username,passphrase)
        if not keys:
            return invalidData
        else:
            session["keys"] = keys
            session["SHA3-256_passphrase"] = passphrase
            session["username"] = username
            return ok
    else:
        return invalidContext

###################################################################
############################ CRITICAL #############################
###################################################################

@app.route("/vote", methods=["POST"])
def vote():
    # Stop Logging Temporarily to anything but errors
    app.logger.setLevel(100) # Higher then **CRITICAL** logs must be send, for them to be logged

    username = session.get("username")
    election = request.values.get('election')
    vote     = request.values.get('vote')

    if username and election and vote:
        Elections.vote(election, vote, username) # After this function is called, nobody has any knowledge of the association between user and vote.

    app.logger.setLevel(0) # The crucial unnoticable part has past.
    # Not even the client is notified, if there was anything wrong, except if they get a timeout.
    return ok

###################################################################
############################ CRITICAL OVER ########################
###################################################################

@app.route("/message", methods=["POST"])
def message():
    author      = session.get("username")
    recipients  = json.loads(request.values.get('to'))
    body        = request.values.get('body')
    keys        = session.get("keys")
    passphrase  = session.get("passphrase")

    if author and recipients and body and keys:
        message =   { "body"    : body
                    , "to"      : recipients
                    , "from"    : author
                    }
        Users.publish( message, keys )

        return ok
    else:
        return invalidData
