from flask import Flask, url_for, redirect, request, g, render_template, session

from Crypto.Hash import SHA256

from functools import wraps
from typing import List
import datetime

from peewee import *
from Server.Database import *

SECRET_KEY  = os.environ["SECRET_KEY"]
DEBUG       = "DEBUG" in os.environ
DATABASE    = os.environ["DATABASE"]

app = Flask ( __name__
            , static_folder     = "static"
            , static_url_path   = "/static"
            , template_folder   = "output"
            )

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
            response = render_template( "login.html", failed_already = failed_already )
        else:
            username    = request.values["username"]
            password    = request.values["password"]

            user        = User.get(User.name == username)
            if user.can_authenticate(password):
                session["authenticated"]    = True
                session["username"]         = user.name
                response = redirect(url_for("index"))
            else:
                response = redirect(url_for("login", failed_already = "true"))
    except KeyError:
        return "data not provided"
    except Exception as e:
        raise e
    else:
        return response

@login_required
@app.route("/", methods=["GET"])
def index():
    try:
        feed        = Message.select().order_by(Message.publishing_date.desc()).dicts()
        message     = request.values.get("message")
        response    = render_template("index.html", feed = feed, message = message)
    except KeyError:
        return "data not provided"
    except Exception as e:
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
        return "data not provided"
    except Exception as e:
        raise e
    else:
        return response

@login_required
@app.route("/vote", methods=["GET"])
def vote_index():
    try:
        elections   = Election.select().where(not Election.closed)
        elections   = list(elections)
        response    = render_template("vote_index.html", elections = elections)
    except Exception as e:
        raise e
    else:
        return response

@login_required
@app.route("/vote/<int:election_id>", methods=["POST","GET"])
def vote(election_id):
    try:
        election    = Election.get(Election.id == election_id)

        if request.method == "GET":
            proposals   = map(lambda p: p["title"], election.proposals)
            response    = render_template("vote.html", proposals = proposals)
        else:
            choice      = json.loads(request.form["choice"])
            voter       = User.get(User.name == session["username"])
            if not voter.vote(election, choice):
                response    = redirect(url_for("index", message="You've already voted"))
            else:
                response    = redirect("/")

    except KeyError:
        return "data not provided"
    except json.JSONDecodeError as json_error:
        return "invalid data format"
    except Exception as e:
        if DEBUG:
            raise e
        else:
            return redirect(url_for("index", message="Sorry, an unknown error occured"))
    else:
        return response

# CREATING ELECTIONS
@login_required
@app.route("/election", methods=["POST", "GET"])
def create_election():
    try:
        if request.method == "GET":
            response                = render_template("create_election.html")
        else:
            title                   = request.form["title"]
            description             = request.form["description"]
            creation_date           = datetime.date.today()
            openning_ballot_date    = creation_date + datetime.timedelta( weeks = 4 )
            closing_date            = creation_date + datetime.timedelta( weeks = 6 )

            Election.create ( title                 = title
                            , description           = description
                            , creation_date         = creation_date
                            , openning_ballot_date  = openning_ballot_date
                            )
    except KeyError:
        return "data not provided"
    except Exception as e:
        raise e
    else:
        return response


@login_required
@app.route("/propose/<int:election_id>", methods=["POST", "GET"])
def propose(election_id):
    try:
        if request.method == "GET":
            response                = render_template("propose.html")
        else:
            election                = Election.get(Election.id == election_id)
            title                   = request.form["title"]
            description             = request.form["description"]
            patches                 = json.loads(request.files["patch"].stream.read().decode("utf-8"))
            author                  = User.get(User.name == session["username"])
            author.propose(election, title, description, patches)
    except KeyError:
        return "file not provided"
    except Exception as e:
        raise e
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
                response    = str(register(username, first_name, last_name, id, password))
        else:
            response    = "invalid user"
    except KeyError:
        return "data not provided"
    except Exception as e:
        g.db.close()
        raise e
    else:
        return response
