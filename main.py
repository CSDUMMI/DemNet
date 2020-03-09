from flask import Flask, url_for, redirect, request

from Crypto.Hash import SHA256

from functools import wraps
from typing import List
import datetime

from peewee import *
from Server.Database import *
 
SECRET_KEY  = os.environ["SECRET_KEY"]
DEBUG       = "DEBUG" in os.environ
DATABASE    = os.environ["DATABASE"]

app = Flask(__name__)
app.config.from_object(__name__)


# Routes used by the average users:
def login_required(f):
    @wraps(f)
    def inner(*args,**kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        else:
            return f(*args,**kwargs)
    return inner

@app.route("/login", methods=["POST", "GET"])
def login():
    try:
        if request.method == "GET":
            failed_already  = request.values["failed_already"] == "true"
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
        feed        = Message.select.order_by(Message.publishing_date.desc()).dicts()
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
@app.route("/vote/<int : election_id>", methods=["POST","GET"])
def vote(election_id):
    try:
        election    = Election.get(Election.id == election_id)

        if request.method == "GET":
            options     = json.loads(election.options)
            response    = render_template("vote.html", options = options)
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

# Creating Elections
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
@app.route("/propose/<int : election_id>", methods=["POST", "GET"])
def propose(election_id):
    try:
        if request.method = "GET":
            response                = render_template("propose.html")
        else:
            election                = Election.get(Election.id == election_id)
            conventional            = request.form["conventional"] == "true"
            title                   = request.form["title"]
            patch                   = request.files["patch"].stream.read().decode("utf-8")
            author                  = User.get(User.name == session["username"])
            author.propose(election, title, patch, conventional)
    except KeyError:
        return "file not provided"
    except Exception as e:
        raise e
    else:
        return response
