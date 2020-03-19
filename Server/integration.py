from Server.Database import *
from peewee import *
from flask import Flask, request

app = Flask(__name__)
app.secret_key  = os.environ["SECRET_KEY"]

@app.route("/hook")
def hook():
    try:

        event   = request.headers.get("X-Gitlab-Event")
        body    = request.get_json()

        if event == "Issue Hook":
            action          = body["object_attributes"]["action"]
            if action == "open" or action == "reopen":
                open_election   = "Hold Election" in map(lambda l: l["title"], body["labels"])
            

        elif event
    except Exception as e:
        raise
    else:
        pass
