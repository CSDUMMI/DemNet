import functools
from typing import List, Tuple

Vote = List[str]
Option = str

"""
Turn class,
a class to collect the current state of the counting.
First it sorts all votes into the options.
If an option is deleted, the votes removed from it
are resorted into the new options.
"""
class Turn():
    def __init__(self,participants : int, votes : List[Vote], options : List[Option]):
        self.__options__ = { key : [] for key in options }
        self.__resort(votes)
        self.participants = participants


    def __resort(self,votes : List[Vote]):
        for vote in votes:
            vote_old = vote
            print(f"Changed from {vote.pop()} to {vote[-1]} in {vote_old}")

            self.__options__[vote[-1]].append(vote)

    def count(self):
        winner = None
        while winner == None:
            least = []
            for option in self.__options__:
                option = (option,len(self.__options__[option]))
                if option[1] > self.participants/2:
                    winner = option
                elif option[1] < sum([s[1] for s in least]):
                    least = option
                elif option[1] == sum([s[1] for s in least]):
                    least.append(option)

            for s in least:
                self.__resort(self.__options__[s[0]])
                print(s[0])
                del self.__options__[s[0]]

        return winner

def count_votes(participants : int, votes : List[Vote], options : List[Option]) -> Tuple[Option, int]:
    turn = Turn(participants,votes,options)
    return turn.count()
