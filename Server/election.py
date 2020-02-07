import functools
from typing import List, Tuple

Vote = List[str]
Option = str

def count_votes( votes : List[Vote], participant_count : int, options : List[Option]) -> Tuple[Option, List[Vote]]:
    turn = map(lambda v: v[-1], votes)
    for i in range(1,len(votes))
        # If one option > 50 % support, it wins
        maximum_option = max([(turn.count(o), o) for o in options])
        if maximum_option[0] > len(votes)/2:
            return (maximum_option[1],filter(lambda v: v[-i] == max(turn)[-i]))# Winner
        else:
            # If no option receives > 50 % support, delete the  least popular ones.
            least_popular_indicies = find_least_popular(turn)
            turn.pop(least_popular_indicies)
            for least_popular_index in least_popular_indicies:
                turn.append(votes[least_popular_index][-i-1])


def find_least_popular( turn : List[Option] ):
    # If the least popular is a singular, just return that:
    turn.index(min(turn))
