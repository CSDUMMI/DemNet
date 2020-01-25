#!/usr/bin/env python3

from Server import Elections, Patches, Users
from flask import Flask, request
from typing import List

app = Flask(__name__, static_url_path="/static", static_folder="/static")
app.secret_key = os.environ["SECRET_KEY"]

@app.route("/login",methods=["POST"])
def login():
    username = request.values.get("username")
    password = request.values.get("password")

    if not session.get("passphrase") and username and password:
        passphrase = Users.login(username,password)
        if not passphrase:
            return 1
        else:
            session["passphrase"] = passphrase
            return 0
    else:
        return 2
