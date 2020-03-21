from flask import Flask, url_for, redirect, request, g, render_template, session
from flaskext.markdown import Markdown
from Crypto.Hash import SHA256

from functools import wraps
from typing import List
import datetime, json, requests

from peewee import *
from Server.Database import *

SECRET_KEY      = os.environ["SECRET_KEY"]
DEBUG           = "DEBUG" in os.environ
DATABASE        = os.environ["DATABASE"]
GITLAB_URI      = os.environ["GITLAB_URI"]
GITLAB_TOKEN    = os.environ["GITLAB_TOKEN"]
DEMNET_ID       = os.environ["DEMNET_ID"]
app = Flask ( __name__
            , static_folder     = "static"
            , static_url_path   = "/static"
            , template_folder   = "output"
            )

md = Markdown(app, extensions=['fenced_code'])
app.config.from_object(__name__)

@app.before_request
def before_request():
    g.db    = database
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response


# Routes used by the average users:
def login_required(f):
    @wraps(f)
    def inner(*args,**kwargs):
        if not session.get("authenticated"):
            return redirect(url_for("login"))
        else:
            return f(*args,**kwargs)
    return inner

@app.route("/login", methods=["POST", "GET"])
def login():
    try:
        if request.method == "GET":
            failed_already  = request.values.get("failed_already") == "true"
            response        = render_template( "login.html", failed_already = failed_already )
        else:
            username        = request.values["username"]
            password        = request.values["password"]
            user            = User.get(User.name == username)
            if user.can_authenticate(password):
                session["authenticated"]    = True
                session["username"]         = user.name
                response                    = redirect("/")
            else:
                raise DoesNotExist()

    except DoesNotExist:
        return redirect(url_for("login", failed_already = "true"))
    except KeyError:
        return "data not provided"
    except Exception as e:
        after_request("")
        raise e
    else:
        return response

@login_required
@app.route("/", methods=["GET"])
def index():
    try:
        feed        = list(Message.select().order_by(-Message.id))
        message     = request.values.get("message")
        response    = render_template("index.html", feed = feed, message = message)
    except KeyError:
        return "data not provided"
    except Exception as e:
        after_request("")
        raise e
    else:
        return response

@login_required
@app.route("/read/<int:message_id>", methods=["GET"])
def read(message_id : str):
    try:
        message         = Message.get(Message.id == message_id)
        publishing_date = message.publishing_date.strftime("%B %d. %Y")
        response        = render_template   ( "read.html"
                                            , message           = message
                                            , publishing_date   = publishing_date
                                            )
    except DoesNotExist:
        return "Message id doesn't exists"
    except Exception as e:
        after_request("")
        raise e
    else:
        return response

@login_required
@app.route("/publish", methods=["POST","GET"])
def publish():
    try:
        if request.method == "GET":
            response    = render_template("publish.html")
        else:

            title       = request.form["title"]
            content     = request.form["content"]
            author      = User.get(User.name == session["username"])

            author.publish(title, content)
            response    = redirect("/")
    except KeyError:
        return "data not provided or not logged in"
    except Exception as e:
        after_request("")
        raise e
    else:
        return response

@login_required
@app.route("/unpublish/<int:message_id>", methods=["POST"])
def unpublish(message_id : int):
    try:
        message = Message.get_by_id(message_id)
        if session["username"] == message.author.name:
            message.delete_instance()
            response    = "Done"
        else:
            response    = "You don't have the right to do this"
    except DoesNotExist:
        return "Doesn't exist"
    except Exception as e:
        after_request("")
        raise e
    else:
        return response
@login_required
@app.route("/vote", methods=["GET"])
def vote_index():
    try:
        stage_1_elections       = Election.select().where(Election.stage == 1)
        stage_2_elections       = Election.select().where(Election.stage == 2)
        response    = render_template("vote_index.html", stage_1_elections = stage_1_elections, stage_2_elections = stage_2_elections)
    except Exception as e:
        after_request("")
        raise e
    else:
        return response

@login_required
@app.route("/vote/<int:election_id>", methods=["POST","GET"])
def vote(election_id):
    try:
        election    = Election.get(Election.id == election_id)

        if request.method == "GET":
            response    = render_template("vote.html", proposals = election.proposals)
        else:
            choice      = json.loads(request.form["vote"])
            voter       = User.get(User.name == session["username"])
            if not voter.vote(election, choice):
                response    = redirect(url_for("index", message="You've already voted"))
            else:
                response    = redirect("/")

    except KeyError:
        return "data not provided"
    except json.JSONDecodeError as json_error:
        return f"invalid data format: {json_error.msg}"
    except Exception as e:
        if DEBUG:
            after_request("")
            raise e
        else:
            return redirect(url_for("index", message="Sorry, an unknown error occured"))
    else:
        return response

# ADMIN ONLY
@login_required
@app.route("/register", methods=["POST","GET"])
def register_route():
    try:
        if session["username"] == "joris":
            if request.method == "GET":
                response    = render_template("register.html")
            else:
                username    = request.values["username"]
                first_name  = request.values["first_name"]
                last_name   = request.values["last_name"]
                id          = request.values["id"]
                password    = request.values["password"]
                response    = str(register(username, first_name, last_name, id, password, connected = true ))
        else:
            response    = "invalid user"
    except KeyError:
        return "data not provided"
    except Exception as e:
        after_request("")
        raise e
    else:
        return response


# WEBHOOKS
@app.route("/hook")
def hook():
    try:

        event   = request.headers.get("X-Gitlab-Event")
        body    = request.get_json()

        if event == "Issue Hook": # Create election
            action          = body["object_attributes"]["action"]
            if action == "open" or action == "reopen":
                open_election   = "Hold Election" in map(lambda l: l["title"], body["labels"])
                if open_election:
                    title           = body["object_attributes"]["title"]
                    description     = body["object_attributes"]["description"]
                    link            = body["object_attributes"]["url"]
                    create_election ( title
                                    , description
                                    , link
                                    )

        elif event == "Merge Request Hook":
            action          = body["object_attributes"]["action"]
            if action == "open":
                title               = body["object_attributes"]["title"].split("-", maxsplit = 1)
                election_id         = int(title[0])
                title               = title[1]
                election            = Election.get_by_id(election_id)

                link                = body["object_attributes"]["url"]
                description         = body["object_attributes"]["description"]
                author              = body["user"]["username"]
                last_commit         = body["object_attributes"]["last_commit"]["id"]
                election.propose( author
                                , link
                                , title
                                , description
                                , last_commit
                                )

                # Protect the source branch
                branch_to_protect   = body["object_attributes"]["source_branch"]
                requests.post   ( f"{GITLAB_URI}/projects/{DEMNET_ID}/protected_branches"
                                , data      =   { "name"                    : branch_to_protect
                                                , "push_access_level"       : 0
                                                , "merge_access_level"      : 0
                                                , "unprotect_access_level"  : 60
                                                }
                                , headers   =   { "Private-Token" : GITLAB_TOKEN
                                                }
                                )




    except ValueError:
        return "Invalid title"
    except Exception as e:
        raise e
    else:
        return "OK"

# CREATING ELECTIONS
def create_election ( title         : str
                    , description   : str
                    , link          : str
                    ):
    try:
        creation_date           = datetime.date.today()
        openning_ballot_date    = creation_date + datetime.timedelta( weeks = 4 )
        closing_date            = creation_date + datetime.timedelta( weeks = 6 )

        Election.create ( title                 = title
                        , description           = description
                        , link                  = link
                        , creation_date         = creation_date
                        , openning_ballot_date  = openning_ballot_date
                        , closing_date          = closing_date
                        )

        response                = "Done"
    except KeyError:
        return "data not provided"
    except Exception as e:
        raise e
    else:
        return response
