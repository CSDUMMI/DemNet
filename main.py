from flask import Flask
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

    def vote( self
            , election : Election
            , choice : List[str]
            ):
        Vote.create(election = election, choice = choice)

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
    username        = CharField()

class Message(BaseModel):
    author          = ForeignKeyField(User, backref="messages")
    title           = TextField()
    content         = TextField()
