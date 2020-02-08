from typing import List, Tuple, TextIO
import sys

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
    def __init__(self,participants : int, votes : List[Vote], options : List[Option], fs : TextIO = None):
        if len(votes) < participants:
            votes.extend([["NoneOfTheOtherOptions"] for x in range(participants-len(votes))])
        self.__options__ = { key : [] for key in options }

        if fs != None:
            self.result_file = fs
        else:
            self.result_file = sys.stdout

        print(f"Votes:\n {votes}\nThrown:", file=self.result_file)

        self.__resort(votes)
        self.participants = participants



    def __resort(self,votes : List[Vote]):
        for vote in votes:

            old = vote.pop()
            if old == "NoneOfTheOtherOptions":
                break
            elif len(vote) == 0:
                self.__options__["NoneOfTheOtherOptions"].append(["NoneOfTheOtherOptions"])
            else:
                self.__options__[vote[-1]].append(vote)

    """count all votes in self.__options__.
    To win the election an option has to have more than limit*100 % support.
    Parameters:
    - threshold : float = 0.5 := Percentages necessary to win for an election
    Returns:
    Either
    - (winner_name,support) : Tuple[str,List[Vote] - If one option has won
    - [(one_winner,support),(other_winner,support)] : List[Tuple[str,List[Vote]]] - If no side could unite the necessary support
    """
    def count(self, threshold : float =0.5):
        winner = None
        while winner == None:
            least = []
            for option in self.__options__:
                option = (option,len(self.__options__[option]))
                if option[1] > self.participants*threshold:
                    winner = option
                elif len(self.__options__) == (1/limit): # another election must be called.
                    keys = list(self.__options__)
                    winner = [(key,self.__options__[key]) for key in keys]
                elif option[1] < sum([s[1] for s in least]):
                    least = option
                elif option[1] == sum([s[1] for s in least]):
                    least.append(option)


            for s in least:
                print(f"{s[0]}",file=self.result_file)
                self.__resort(self.__options__[s[0]])
                self.__options__.pop(s[0],None)

        print(f"Winner:\n{winner[0]}, {winner[1]}", file=self.result_file)
        return winner

def count_votes(participants : int, votes : List[Vote], options : List[Option], fs : TextIO = None, threshold : float = 0.5) -> Tuple[Option, int]:
    turn = Turn(participants,votes,options, fs)
    result = turn.count(threshold=threshold)

    if fs != None:
        fs.close()

    return result
