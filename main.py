#!/usr/bin/env python3

from Server import Elections, Patches, Users.py
from flask import Flask

app = Flask(__name__, static_url_path="/static", static_folder="/static")
app.secret_key = os.environ["SECRET_KEY"]

@app.route("/login",methods=["POST"])
def login():
    
