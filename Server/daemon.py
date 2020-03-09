#!/usr/bin/env python3
# Executes every day at 00:00 (midnight)
from peewee import *
import datetime, subprocess, io, sys

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

def implement_proposal(proposal : Proposal):
    # Apply each patch.
    for patch in proposal.patches.select().order_by(Patch.index):
        repo        = LAWS_REPO if patch["conventional"] else SOURCE_REPO
        patch_text  = io.StringIO(initial_value=patch["text"])

        subprocess.run(["git", "apply", "-"], stdin=patch_text, cwd=repo)

    # Add a commit with the new Change Log
    log_message = f"""[{str(datetime.date.today())}] {proposal.title}
By {proposal.author}
{proposal.description}
"""
    open(f"{LAWS_REPO}/CHANGELOG", "a").write(log_message)
    open(f"{SOURCE_REPO}/CHANGELOG", "a").write(log_message)

if sys.argv[1] == "e" or sys.argv[1] == "execute":
    close_elections()
    database.close()
