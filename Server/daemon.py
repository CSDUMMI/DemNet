#!/usr/bin/env python3
# Executes every day at 00:00 (midnight)
from peewee import *
import datetime, subprocess, io

from Server.Database import *
from Server.election import count

DATABASE    = os.environ["DATABASE"]

SOURCE_REPO = os.environ["SOURCE_REPO"] # Git Repo of the source code, not where this is stored. (for applying conventional = False proposals)
LAWS_REPO   = os.environ["LAWS_REPO"] # Git Repo of the conventional laws. (for applying conventional = True proposals)

database    = SqliteDatabase(DATABASE)
database.connect()

# Close, count and apply all changes.
def close_elections():
    closed_elections    = Election.select().where(
                                    Election.closing_date <= datetime.date.today \
                                    and not Election.closed
                                    )

    for closed_election in closed_elections:
        votes       = list(map(lambda v: json.loads(v),closed_election.votes))
        proposals   = list(map(lambda p:p["title"], closed_election.proposals))
        winner      = count(votes, proposals)
        closed_election.winner = str(winner)
        closed_election.save()
        # Implement changes
        if winner != None:
            winner      = closed_election.proposals.get(Proposal.title == str(winner))
            implement_proposal(winner)
            Change_Log.create   ( election  = closed_election
                                , message   = f"Title:{winner.title}\nAuthor:{winner.author}\nDescription{winner.description}"
                                , date      = datetime.date.today()
                                )
        else:
            Change_Log.create(election = closed_election, message = "No one won")
