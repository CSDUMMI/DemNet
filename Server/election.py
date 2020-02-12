from typing import List, Tuple, TextIO, Any
import sys, json, functools

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
    def __init__(self, votes : List[Vote], participants : int, options : List[Option], fs : TextIO = None):
        self.participants = participants
        self.__options__ = { key : list(filter(lambda v: v[-1] == key)) for key in options }


    def order(self,reverse=False):
        return sorted(list(self.__options__), key = lambda k: len(self.__options__[k]), reverse=reverse)

    def __resort(self,votes : List[Vote]):
        for vote in votes:
            vote.pop()
            if vote != []:
                self.__options__[vote[-1]].append(vote)
            else:
                self.potential_voters += 1

    """count all votes in self.__options__.
    It follows the following principle:
    Each turn one or more options are selected
    to be eliminated.
    In elimination, all votes, that are voting for the option are reallocated
    to the next alternative option choice.
    Once an option reached a threshold of support, the counting is over.

    To win the election an option has to have more than limit*100 % support.
    Returns:
    Either
    - (winner_name,support) : Tuple[str,List[Vote] - If one option has won
    - [(one_winner,support),(other_winner,support)] : List[Tuple[str,List[Vote]]] - If no side could unite the necessary support
    - False - If Error has occured and invalid data been provided.
    """
    def count(self):
        threshold = 0.5
        winner = False
        while type(winner) != "" or winner != None:
            ordered = self.order(reverse=True)
            if len(self.__options__[ordered[0]]) > (participants*threshold):
                winner = ordered[0]
            elif len(self.__options__[ordered[o]]) == (participants*threshold) and len(self.__options__[ordered[1]]) == (participants*threshold):
                winner = None
            elif self.potential_voters/self.participants > threshold:
                winner = None
            else:
                least = self.least()
                for l in least:
                    self.__resort(self.__options__[l])
                    self.__options__.pop(l)

    def least(self):
        ordered = self.order()
        least = ([ordered[0]], len(self.__options__[ordered[0]]))

        for o in ordered:
            support_for_o = len(self.__options__[o])
            if support_for_o < least[1]:
                least = (o,support_for_o)
            elif support_for_o == least[1]:
                least[0].append(o)
                least[1] += support_for_o
            elif support_for_o > least[1]:
                continue

        return least[0]



def count_votes(participants : int, votes : List[Vote], options : List[Option], fs : TextIO = None) -> Tuple[Option, int]:
    turn = Turn(participants,votes,options, fs)
    result = turn.count()

    if fs != None:
        fs.close()

    return result
