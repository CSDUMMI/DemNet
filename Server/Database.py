import os, datetime
from peewee import *

DATABASE    = os.environ["DATABASE"]
database    = SqliteDatabase(DATABASE)

class BaseModel(Model):
    class Meta():
        database    = database

class User(BaseModel):
    name        = CharField(unique=True)
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
        if Participant.select().where(user == self).count() == 0 or :
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


class Election(BaseModel):
    id                      = IntegerField(unique = True, index = True, primary_key = True)
    title                   = TextField()
    description             = TextField()
    closed                  = BooleanField(default = False)
    winner                  = TextField(default = None)
    creation_date           = DateField()
    openning_ballot_date    = DateField()
    closing_date            = DateField()

class Vote(BaseModel):
    election                = ForeignKeyField(Elections, backref="votes")
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
    with database:
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
