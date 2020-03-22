import os, datetime
from peewee import *
from typing import List, Dict
from urllib.parse import urlparse

from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes

DATABASE_URL    = urlparse(os.environ["DATABASE_URL"])

DATABASE_NAME   = DATABASE_URL.path[1:]
username        = DATABASE_URL.username
password        = DATABASE_URL.password
host            = DATABASE_URL.hostname

database        = PostgresqlDatabase( DATABASE_NAME
                                    , user      = username
                                    , password  = password
                                    , host      = host
                                    , sslmode   = "require"
                                    )
class BaseModel(Model):
    class Meta():
        database    = database

class Election(BaseModel):
    id                      = IntegerField(unique = True, primary_key = True)
    title                   = TextField()
    description             = TextField()
    link                    = TextField()
    stage                   = IntegerField(default = 1)
    winner                  = TextField(default = None, null=True)
    creation_date           = DateField()
    openning_ballot_date    = DateField()
    closing_date            = DateField()
    def propose ( self
                , author        : str
                , link          : str
                , title         : str
                , description   : str
                , last_commit   : str
                ):
        Proposal.create ( election      = self
                        , link          = relative_link
                        , title         = title
                        , description   = description
                        , author        = author
                        , last_commit   = last_commit
                        )

class User(BaseModel):
    name        = CharField(unique = True, primary_key = True)
    first_name  = TextField()
    last_name   = TextField()
    id          = CharField(unique = True)
    password    = CharField()
    salt        = FixedCharField(max_length = 64)

    def publish(self, title : str, content : str):
        Message.create  ( author            = self
                        , title             = title
                        , content           = content
                        , publishing_date   = datetime.date.today()
                        )
        return True

    def can_authenticate(self, password : str) -> bool:
        password = hash_passwords(password, self.salt)
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


class Proposal(BaseModel):
    election                = ForeignKeyField(Election, backref="proposals")
    link                    = TextField()
    title                   = TextField()
    description             = TextField()
    author                  = TextField()
    last_commit             = FixedCharField(max_length=40)


class Vote(BaseModel):
    election                = ForeignKeyField(Election, backref="votes")
    choice                  = TextField()

class Participant(BaseModel):
    election                = ForeignKeyField(Election, backref="participants")
    user                    = ForeignKeyField(User, backref="participation")

class Message(BaseModel):
    author                  = ForeignKeyField(User, backref="messages")
    id                      = IntegerField(primary_key = True, index = True)
    title                   = TextField()
    content                 = TextField()
    publishing_date         = DateTimeField()

class Change_Log(BaseModel):
    election                = ForeignKeyField(Election, backref="logs")
    message                 = TextField()
    date                    = DateField()

def hash_passwords(password : str, salt : str) -> bytes:
    return SHA256.new(data = password.encode("utf-8") + salt.encode("utf-8")).hexdigest()

def register( username      : str
            , first_name    : str
            , last_name     : str
            , id            : str
            , password      : str
            , connected     : bool  = False
            ):
            try:
                if not connected:
                    database.connect()
                id          = hash_passwords(id, "")
                salt        = SHA256.new(data = get_random_bytes(2**3)).hexdigest()
                password    = hash_passwords(password, salt)

                if User.select().where(User.id == id or User.name == user).count() >= 1:
                    response    = False
                else:
                    User.create ( name          = username
                                , first_name    = first_name
                                , last_name     = last_name
                                , id            = id
                                , password      = password
                                , salt          = salt
                                )
                    response    = True
                if not connected:
                    database.close()
            except Exception as e:
                raise e
            else:
                return response


def create_tables():
    try:
        database.connect()
        database.create_tables( [ User
                                , Election
                                , Vote
                                , Participant
                                , Proposal
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

if not Election.select().exists():
    create_tables()
