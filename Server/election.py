import functools
from typing import List, Tuple

Vote = List[str]
Option = str

def count_votes( votes : List[Vote], participant_count : int, options : List[Option]) -> Tuple[Option, List[Vote]]:
    return (options[0],votes)
