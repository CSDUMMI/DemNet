#!/usr/bin/env python3

import sys
import Patches
from election import count_votes
from pymongo import MongoClient

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
If the Changes have human-readable laws the field
"human-readable" is filled with an array of Law elements:
This can be of three kinds:
- "Remove Law" + <law_id>
- { "id" : SHA256(this)
  , "paragraphs" : ["<§1>","<§2>",etc.]
  ,
  }
"""
def create(type,options):
    if type == "human-readable":

    elif type == "executable":

    else:
        print("Error: Invalid type in Election", file=sys.stderr)
