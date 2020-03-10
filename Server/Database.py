import os, datetime
from peewee import *
from typing import List, Dict

from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes

DATABASE    = os.environ["DATABASE"]
database    = SqliteDatabase(DATABASE)

class BaseModel(Model):
    class Meta():
        database    = database

class Election(BaseModel):
    id                      = IntegerField(unique = True, index = True, primary_key = True)
    title                   = TextField()
    description             = TextField()
    closed                  = BooleanField(default = False)
    winner                  = TextField(default = None)
    creation_date           = DateField()
    openning_ballot_date    = DateField()
    closing_date            = DateField()

class User(BaseModel):
    name        = CharField(unique = True)
    first_name  = TextField()
    last_name   = TextField()
    id          = CharField(unique = True)
    password    = CharField()
    salt        = FixedCharField(max_length = 2**3)

    def publish(self, title : str, content : str):
        Message.create  ( author    = self
                        , title     = title
                        , content   = content
                        )
        return True

    def can_authenticate(self, password : str):
        password = SHA256.new(data = password.encode("utf-8") + self.salt.encode("utf-8")).hexdigest()
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

    def propose(self, election : Election, title : str, description : str, patches):
        if election.openning_ballot_date < datetime.date.today():
            proposal = Proposal.create  ( author        = self
                                        , election      = election
                                        , title         = title
                                        , description   = description
                                        )

            for index, patch in enumerate(patches):
                Patch.create( proposal      = proposal
                            , patch         = patch["text"]
                            , conventional  = patch["conventional"] == "true"
                            , index         = index
                            )
            return True
        else:
            return False


class Vote(BaseModel):
    election                = ForeignKeyField(Election, backref="votes")
    choice                  = TextField()

class Participant(BaseModel):
    election                = ForeignKeyField(Election, backref="participants")
    user                    = ForeignKeyField(User, backref="participation")

class Proposal(BaseModel):
    election                = ForeignKeyField(Election, backref="proposals")
    author                  = ForeignKeyField(User, backref="proposals")
    title                   = CharField(unique = True)
    description             = TextField()

class Patch(BaseModel):
    proposal                = ForeignKeyField(Proposal, backref="patches")
    patch                   = TextField()
    index                   = IntegerField()
    conventional            = BooleanField()

class Message(BaseModel):
    author                  = ForeignKeyField(User, backref="messages")
    title                   = TextField()
    content                 = TextField()
    publishing_date         = DateTimeField()

class Change_Log(BaseModel):
    election                = ForeignKeyField(Election, backref="logs")
    message                 = TextField()
    date                    = DateField()

def create_tables():
    try:
        database.connect()
        database.create_tables( [ User
                                , Election
                                , Vote
                                , Participant
                                , Proposal
                                , Patch
                                , Message
                                , Change_Log
                                ]
                                )
        database.close()
    except OperationalError:
        return False
    except Exception as e:
        raise e
    else:
        return True

def register( username      : str
            , first_name    : str
            , last_name     : str
            , id            : str
            , password      : str
            ):
            id          = SHA256.new(data = id.encode("utf-8")).hexdigest()
            password    = SHA256.new(data = password.encode("utf-8")).hexdigest()
            salt        = str(get_random_bytes(2**3))

            if User.select().where(User.id == id or User.name == user).count() >= 1:
                return False
            else:
                User.create ( name          = username
                            , first_name    = first_name
                            , last_name     = last_name
                            , id            = id
                            , password      = password
                            , salt          = salt
                            )
                return True
