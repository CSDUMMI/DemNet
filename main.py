from flask import Flask, url_for, redirect, request, g, render_template, session
from flask_mistune import Mistune, markdown

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

md          = Mistune(app)

app.config.from_object(__name__)

@app.before_request
def before_request():
    g.db    = database
    g.db.connect()
    update_elections()

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

@login_required
@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    try:
        if request.method == "GET":
            response                = render_template("change_password.html")
        else:
            user                    = User.get(User.name == session["username"])
            password                = request.form["password"]
            password                = hash_passwords(password, user.salt)
            new_passsword           = request.form["new_passsword"]
            new_repeated_password   = request.form["new_repeated_password"]
            if password == user.password:
                if new_passsword == new_repeated_password:
                    new_salt            = SHA256.new(data = get_random_bytes(2**3)).hexdigest()
                    new_passsword       = hash_passwords(new_passsword, new_salt)
                    user.password       = new_passsword
                    user.salt           = new_salt
                    user.save()
                    response            = "Done"
                else:
                    response            = "Passwords don't match"
            else:
                response    = "Invalid current password"
    except KeyError:
        return "Data not provided"
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
                response    = str(register(username, first_name, last_name, id, password, connected = True ))
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
@app.route("/hook", methods=["GET", "POST"])
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
                    id              = body["object_attributes"]["iid"]
                    create_election ( title
                                    , description
                                    , link
                                    , id
                                    )
            elif action == "close":
                if "Hold Election" in map(lambda l: l["title"], body["labels"]):
                    id              = body["object_attributes"]["iid"]
                    election        = Election.get_by_id(id)

                    if election and election.openning_ballot_date > datetime.date.today():
                        election.delete_instance()

        elif event == "Merge Request Hook":
            action          = body["object_attributes"]["action"]
            if action == "open":
                # Title: #<election_id>:<title>
                try:
                    title               = body["object_attributes"]["title"].split(":", maxsplit = 1)
                    election_id         = int(title[0][1:])
                    title               = title[1]
                    election            = Election.get_by_id(election_id)

                    id                  = body["object_attributes"]["iid"]
                    link                = body["object_attributes"]["url"]
                    description         = body["object_attributes"]["description"]
                    author              = body["user"]["username"]
                    last_commit         = body["object_attributes"]["last_commit"]["id"]

                    election.propose( author
                                    , id
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
                    # Invalid format for title
                    iid                 = body["object_attributes"]["iid"]
                    req                 = requests.delete   ( f"{GITLAB_URI}/projects/{DEMNET_ID}/merge_requests/{iid}"
                                                            , headers   = { "Private-Token" : GITLAB_TOKEN }
                                                            )

                except Exception as e:
                    raise e




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
                    , id            : int
                    ):
    try:
        creation_date           = datetime.date.today()
        openning_ballot_date    = creation_date + datetime.timedelta( weeks = 4 )
        closing_date            = creation_date + datetime.timedelta( weeks = 6 )

        Election.create ( id                    = id
                        , title                 = title
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

# CLOSING / MERGING ELECTIONS
def update_elections():
    elections   = Election.select().where(Election.openning_ballot_date >= datetime.date.today() and Election.stage == 1)
    for election in elections:
        election.stage = 2
        election.save()

    elections   = Election.select().where(Election.closing_date <= datetime.date.today() and Election.stage == 2)
    for election in elections:
        votes       : List[List[str]]   = [json.loads(v.choice) for v in election.votes]
        proposals   : List[str]         = [p.title for p in election.proposals]

        winner                          = count(votes, proposals)
        winner                          = Proposal.get(Proposal.title == winner)
        id                              = winner.id

        req     = requests.put  ( f"{GITLAB_URI}/projects/{DEMNET_ID}/merge_requests/{id}/merge"
                                , params    =   { "sha"                         : winner.last_commit
                                                , "should_remove_source_branch" : True
                                                }
                                , headers   =   { "Private-Token" : GITLAB_TOKEN }
                                )

        if not req.status_code == 200:
            print(f"Error {req.status_code}")
