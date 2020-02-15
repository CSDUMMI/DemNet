import random, pyrankvote, pprint
from typing import List, Dict
from pyrankvote import Candidate, Ballot

def vote(votes : List[List[str]], options : List[str]):
    options = { key : list(filter(lambda v: v[-1] == key, votes)) for key in list(options) }
    votes = len(votes)
    result = { "removed_votes" : 0
             , "winner" : False
             , "rounds" : []
             }
    while result["winner"] == False:
        winners = list(filter(lambda o:len(o)/votes > 0.5, options))
        result["rounds"].append(options)
        if winners != []:
            if len(winners) == 1:
                result["winner"] = winners[0]
            else:
                result["winner"] = None
            break
        else:
            least = sorted(list(options), key=lambda o: len(options[o]))
            print(least)
            least = options.pop(least[-1])

            options = { key : list(filter(lambda a: a != least, options[key])) for key in list(options) }
            result["removed_votes"] = votes - sum([len(option) for option in options])
            votes = sum([len(option) for option in options])
            continue

    return result

def test(n):
    options = ["A","B","C","D"]
    votes = [random.sample(options,k=random.randint(1,len(options))) for i in range(n)]
    result = vote(votes,options)["winner"]
