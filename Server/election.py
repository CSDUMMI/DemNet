from typing import List, Tuple, TextIO, Any
import sys, json, functools

Vote = List[str]
Option = str


"""
"""


def count_votes(participants : int, votes : List[Vote], options : List[Option], fs : TextIO = None) -> Tuple[Option, int]:
    election = Election(participants,votes,options, fs=fs)
    result = election.count()

    if fs != None:
        fs.close()

    return result
