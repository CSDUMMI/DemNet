#!/usr/bin/env python3

from Server import Elections, Patches, Users
from flask import Flask, request, render_template, session, redirect
import pymongo
from pymongo import MongoClient
import json, os
from Crypto.Hash import SHA3_256

app = Flask( __name__
           , static_url_path="/static"
           , static_folder="output/static"
           , template_folder="output")
app.secret_key = os.environ["SECRET_KEY"]

client              = MongoClient()
db                  = client.demnet
messages            = db.messages
users               = db.users
# Errors
debug                       = os.environ.get("DEBUG")
errors = { "OK"                         : "0"
         , "error_for_unknown_reason"   : "1"
         , "error_but_not"              : "2"
         , "invalid_data"               : "3"
         , "invalid_context"            : "4"
         , "not_logged_in"              : "5"
         }

errors = { key : errors[key] if not debug else key for key in errors }


"""
Returns either the login.html
or feed.
If the user is logged in, returns feed
sorted by most recent uploads as
dict of "title" and "hash".
So you can use /read/<hash> to get to reading that upload.
"""
@app.route("/", methods=["GET"])
def index():
    try:
        sorted_messages     = sorted(list(messages.find({})),key=lambda m: m["upload_time"], reverse=True)
        sorted_messages     = list(map( lambda m:       { "title" : m["body"]["title"]
                                                        , "hash" : m["hash"] }
                                                        , sorted_messages
                                    )
                                )
        print(sorted_messages)
        response =  render_template ( "index.html"
                                    , messages  = sorted_messages
                                    , logged_in = session.get("username") != None
                                    )

    except Exception as e:
        raise e
    else:
        return response


@app.route("/login", methods=["GET", "POST"])
def login():
    try:
        if request.method == "GET":
            return render_template("login.html")
        elif request.method == "POST":
            username = request.values["username"]
            password = request.values["password"]

            sha3_256            = SHA3_256.new()
            sha3_256.update(password.encode('utf-8'))
            passphrase          = sha3_256.hexdigest()
            keys                = Users.login( username, passphrase )
            session["keys"]     = keys
            session["username"] = username
            response            = redirect("/")

    except KeyError:
        return errors["invalid_data"]
    except Exception as e:
        raise e
    else:
        return response

"""
Returns the readings-index.html template
with template argument:
    readings : List[Tuple[title,hash of reading]]

"""
@app.route("/readings", methods=["GET"])
def readings():
    try:
        readings    = users.find_one({ "username" : session["username"] })["readings"]
        readings    = [messages.find_one({ "hash" : reading }) for reading in readings]
        readings    = [(reading["body"]["title"], reading["hash"]) for reading in readings]
        response    = render_template("readings-index.html", readings=readings)
    except KeyError:
        return errors["not_logged_in"]
    except Exception as e:
        raise e
    else:
        return response

"""
Returns the reading.html template
with argument:
    reading, the full message.
"""
@app.route("/read/<reading_hash>", methods=["GET"])
def read(reading_hash):
    try:
        reading     = messages.find_one({ "hash" : reading_hash })
        response    = render_template("reading.html", reading=reading)
    except Exception as e:
        raise e
    else:
        return response

###################################################################
############################ CRITICAL #############################
###################################################################

@app.route("/vote", methods=["POST"])
def vote():
    try:
        app.logger.setLevel(100)

        if session.get("username"):
            raise "invalid_context"
        username = session["username"]
        election = request.values['election']
        vote     = request.values['vote']

        Elections.vote(election, vote, username)
        app.logger.setLevel(0)
    except "invalid_context":
        return errors["invalid_context"]
    except KeyError:
        return errors["invalid_data"]
    else:
        return errors["OK"]

###################################################################
############################ /CRITICAL ############################
###################################################################

@app.route("/message", methods=["POST"])
def message():
    try:
        if not session.get("username") or not session.get("keys"):
            raise "invalid_context"

        author      = session["username"]
        body        = json.loads(request.values["body"])
        keys        = session["keys"]

        message     =   { "body"    : body
                        , "from"    : author
                        }

        Users.publish( message, keys )

    except KeyError:
        return errors["invalidData"]
    except "invalid_context":
        return errors["invalid_context"]
    except Exception as e:
        raise e
    else:
        return errors["OK"]
