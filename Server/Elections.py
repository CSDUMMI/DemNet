#!/usr/bin/env python3

import sys
import Patches
from election import count_votes
from pymongo import MongoClient
from Crypto.Hash import SHA256

"""
To create, count and handle victory conditions.

There are two kinds of elections,
as there are two kinds of laws:
Executable and Human Readable.

Executable Law is Source Code,
that must be just as approved as Textual, Human Readable to be more percise,
Law. But they have to be handled differently on this level.

Human-readable laws are:
- Changes to right/wrong questions (laws in the juristical sense)
- Proposal for a Patch (pre-election)

Executable laws are:
- Fully developed patches, that must be voted on.

# All changes, in general
All changes change laws and depending on
whether those laws are executable or human-readable
they have to differ somewhat.
These fields they have in general though:
- simple_description, simple, brief language
to get an overview of the changes
- long_description, conclusive, may even complex, description.
A bad long_description is one that is written with the intent
to promote the change.

# Human-Readable Changes
Human Readable Laws consist of paragraphs.
If the Changes have human-readable laws the argument
is filled with an array of Law elements:
This can be of three kinds:
- { "type" : "Remove", "id" : <law_hash> }
- { "type" : "New",
    "law" : { "title" : <title>
            , "paragraphs" : [<§1>,<§2>]
            }
  }
- { "type" : "Ammend"
  , "to" : <law_hash>
  , "ammendment" : [<§1 ammended>, <§2 ammended> ]
  }

A "Remove" Change removes a law with the hash.
A "New" Change is a totally new law with the given paragraphs.
An "Ammend" Change ammends the given paragraphs to an existing law.

# Executable Changes
If a patcher has done their duty,
they propose the final election.
Then the patch folder locked, they
won't be able to edit it anymore.
Thus if a Executable change is proposed,
the executable_changes must be filled with
[
    { "patcher" : <patcher's name>
    , "patch" : <patch name>
    , "conclusion" : <description to describe the final patch>
    }
]
You can't combine two patches and make a vote on the
two together, but you can propose two alternatives,
which are then put into this list.
"""
def create(simple_description, long_description, human_readable_changes, executable_changes):
    client = MongoClient()
    db = client.demnet
    elections = db.elections

    if human_readable_changes == [] and executable_changes == []:
        return None
    else:
        election =  { "long_description" : long_description
                    , "simple_description" : simple_description
                    , "human_readable_changes" : human_readable_changes
                    , "executable_changes" : executable_changes
                    , "participants" : []
                    , "votes" : []
                    }
        election['hash'] = SHA256.new(election).hexdigest()
        elections.insert_one(election)
        return election['hash']

def vote()
