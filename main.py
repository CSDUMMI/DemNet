from flask import Flask, url_for, redirect, request
from functools import wraps
from peewee import *
from Crypto.Hash import SHA256
from typing import List

SECRET_KEY  = os.environ["SECRET_KEY"]
DEBUG       = "DEBUG" in os.environ
DATABASE    = os.environ["DATABASE"]

app = Flask(__name__)
app.config.from_object(__name__)

database    = SqliteDatabase(DATABASE)

class BaseModel(Model):
    class Meta():
        database    = database

class User(BaseModel):
    username    = CharField(unique=True)
    id          = CharField(unique=True)
    password    = CharField()
    salt        = CharField()

    def publish(self, title : str, content : str):
        Message.create  ( author    = self
                        , title     = title
                        , content   = content
                        )
        return True

    def can_authenticate(self, password : str):
        password = SHA256.new()
            .update(password.encode("utf-8") + self.salt.encode("utf-8"))
            .hexdigest()
        if password == self.password:
            return True
        else:
            return False

    def vote(self, election : Election, choice : List[str]):
        if Participant.select().where(user == self).count() == 0:
            Vote.create ( election = election
                        , choice = json.dumps(choice)
                        )
            Participant.create  ( election  = election
                                , user      = self
                                )
            return True
        else:
            return False


class Election(BaseModel):
    options         = TextField()
    title           = TextField()
    description     = TextField()
    creation_date   = DateField()
    closing_date    = DateField()

class Vote(BaseModel):
    election        = ForeignKeyField(Elections, backref="votes")
    choice          = TextField()

class Participant(BaseModel):
    election        = ForeignKeyField(Election, backref="participants")
    user            = ForeignKeyField(User, backref="participation")

class Message(BaseModel):
    author          = ForeignKeyField(User, backref="messages")
    title           = TextField()
    content         = TextField()


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
    if request.method == "GET":
        failed_already  = request.values["failed"] == "true"
        return render_template( "login.html",
                                failed_already=failed_already)
    else:
        username    = request.values["username"]
        password    = request.values["password"]

        user        = User.get(User.username == username)
        if user.can_authenticate(password):
            session["authenticated"] = True
            return redirect("/")
        else:
            return redirect("/login")
