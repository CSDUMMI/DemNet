from typing import List, Tuple, TextIO, Any
import sys, json

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
        if len(votes) < participants:
            votes.extend([["NoneOfTheOtherOptions"] for x in range(participants-len(votes))])

        self.threshold = 0.5
        self.__options__ = { key : list(filter(lambda v:v[-1] == key, votes)) for key in options }
        if "NoneOfTheOtherOptions" not in list(self.__options__):
            self.__options__["NoneOfTheOtherOptions"] = []
        if fs != None:
            self.result_file = fs
        else:
            self.result_file = sys.stdout

        print(f"Votes:\n {json.dumps(votes)}\nThrown:", file=self.result_file)


        self.participants = participants



    def __resort(self,votes : List[Vote]):
        for vote in votes:

            old = vote[-1]
            if old == "NoneOfTheOtherOptions":
                continue
            elif len(vote) == 1:
                self.__options__["NoneOfTheOtherOptions"].append(["NoneOfTheOtherOptions"])
            else:
                vote.pop()
                self.__options__[vote[-1]].append(vote)

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
        winner = None
        is_infinite_loop = 0
        while winner == None:
            winners = list(filter(lambda o: (len(self.__options__[o])/self.participants > threshold),self.__options__))
            if len(winners) == 1:
                winner = winners[0]
            elif len(winners) == 2:
                winner = winners
            else:
                least = self.least()
                for s in least:
                    print(f"{s[0]}",file=self.result_file)
                    self.__resort(self.__options__[s[0]])

                    # If not all instances of this option are removed, KeyErrors
                    # would be thrown once count() meet them again.
                    for option in self.__options__:
                        self.__options__[option] = [[alternative for alternative in v if alternative != s] for v in self.__options__[option]]
                    self.__options__.pop(s[0],None)

        if type(winner) == type(""):
            winner = (winner, len(self.__options__[winner])/self.participants)

        print(f"Winner:\n{winner}", file=self.result_file)
        return winner

    def least(self):
        options = list(self.__options__)
        least = [options[0]]
        for o in options[1:]:
            sub_support_of_o_from_least_support = (len(self.__options__[o])/self.participants) - sum([len(self.__options__[least_option]) for least_option in least])
            if (sub_support_of_o_from_least_support > 0) or (o == "NoneOfTheOtherOptions"):
                # Ignore this option
                continue
            elif sub_support_of_o_from_least_support == 0:
                least.append(o)
            elif sub_support_of_o_from_least_support < 0:
                least = [o]

        return least

def count_votes(participants : int, votes : List[Vote], options : List[Option], fs : TextIO = None) -> Tuple[Option, int]:
    turn = Turn(participants,votes,options, fs)
    result = turn.count()

    if fs != None:
        fs.close()

    return result
