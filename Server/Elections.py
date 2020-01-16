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
"""
def create(type,options):
    if type == "human-readable":
    elif type == "executable":

    else:
        print("Error: Invalid type in Election", file=sys.stderr)
