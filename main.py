#!/usr/bin/env python3

from Server import Elections, Patches, Users
from flask import Flask, request
from typing import List
from Crypto.Hash import SHA3_256

app = Flask(__name__, static_url_path="/static", static_folder="/static")
app.secret_key = os.environ["SECRET_KEY"]

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
            return 1
        else:
            session["keys"] = keys
            session["SHA3-256_passphrase"] = passphrase
            return 0
    else:
        return 2
