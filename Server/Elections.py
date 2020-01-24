#!/usr/bin/env python3

import sys, time, sched, subprocess, json
import Patches
from election import count_votes
from pymongo import MongoClient
from Crypto.Hash import SHA256


"""
Utility function to get the MongoClient.demnet[<collection>]
"""
def collection(collection_name):
    client = MongoClient()
    db = client.demnet
    return db[collection_name]

"""
Scheduler for all Elections close call on deadline
"""
scheduler = sched.scheduler(time.time,time.sleep)

"""
To create, count and handle victory conditions.

# An Election
On all elections there are at least two options:
1. Proposal 1
2. None of the Other options
There can be more Proposals, but if None of the other Options
wins, nothing happens.
Each Election has this field filled:
- deadline, unix timestamp of the end of voting

All Proposals in an Election can either be:
1. Human Executable
2. Machine Executable

A Human Executable Proposal is:
{ "removals" : [<law hashes>]
, "new" : [{ "title" : <title>, "paragraphs" : [<§1>,<§2>,…] }]
, "ammendments" : [{ "law" : <hash of existing law>, "paragraphs" : [<§1 ammended>, <§2 ammended> ...] }]
, "description" : <markdown description of the Proposal in simple terms>
}
Removals are all the Human Executable Laws, that  should be
removed by the Proposal.
"new" Laws are totally new Laws, that should apply
if the Proposal is approved.
Ammendments are Paragraphs, that are added to an existing law at the end.

An Machine Executable Proposal is
a reference to a path of the Git Repo relative to $PATCHES/
If a proposal is created for a Patch, then the Git Repo cannot
be modified. (chmod a-w <path/to/repo>)
Thus a Proposal would look like this:
{ "patch_id" :  "<hash field of the patch in demnet.patches" }

# The Law Database
A approved Law in the Database demnet.laws
"""
def create(type,deadline,proposals):
    election = { "proposals" : proposals
               , "deadline" : deadline
               , "closed" : False
               , "winner" : None
               , "type" : type
               }
    if type == "machine":
        patches = collection("patches")
        for proposal in proposals:
            patch = patches.find_one({ "hash" : proposal['patch_id'] })
            if patch:
                absolute_path = f"{os.environ['PATCHES']}/{patch['patcher']}-{patch['name']}"""
                subprocess.run("chmod a-w", absolute_path) # Block any writing to the repository
            else:
                # Remove proposals, that don't exist
                election['proposals'].remove(proposal)
    elif type == "human":
        # Requiements for a human executable law
        # **All referenced laws and the book have to exist**
        laws = collection("laws")
    elections = collection("elections")
    election['hash'] = SHA256.new(data=json.dumps(election).encode('utf-8')).hexdigest()
    if elections.find_one({ 'hash' : election['hash'] }):
        # If the same Election was proposed already,
        # reject the election.
        # Be aware, this doesn't prevent proposing an
        # election later with a different deadline.
        # But it prevents spamming elections.
        return False
    else:
        scheduler.enter(deadline-time.time(),0, close, argument=(election['hash']))
        elections.insert_one(election)
        return election['hash']

"""
a vote is a list of all options ranked by
how much a voter wants them to win. (see alternative vote).
**This function call cannot leave any trace of the association between
username and vote.**
"""
def vote(election_hash,vote,username):
    elections = collection("elections")
    election = elections.find_one({ "hash" : election_hash })

    if username in election["participants"] and not election['closed']:
        return False
    else:
        elections.update_one({ "hash" : election_hash }, { "$push" : { "participants" : username }})
        elections.update_one({ "hash" : election_hash }, { "$push" : { "votes" : vote }})
        return True


"""
Closing an election means:
Calculating the results and publishing
them.
Publishing the votes, to make the independent control
possible.
"""
def close(election_hash):
    elections = collection('elections')
    election = elections.find_one({ "hash" : election_hash })

    if election:
        if election.get('deadline') <= time.time():
            winner = count_votes(election.votes, len(election.participants), range(0,len(election.proposals)+1))["ballot"]
            winner = election.proposals[winner]
            elections.update_one({ "hash" : election_hash }, { "$set" : { "winner" : winner, "closed" : True } })

            if election['type'] == "machine":
                patches = collection('patches')
                patch = patches.find_one({ "hash" : winner['patch_id'] })
                Patches.close(patch['name'], patch['name'], patch['hash'], merge=True)
            elif election['type'] == "human":
                laws = collection("laws")
                # Append ammendments to laws
                for ammendment in winner["ammendment"]:
                    law = laws.update_one({ "book" : winner["book"], "law" ammendment["law"] }
                                         , { })

            return True
    else:
        return False
