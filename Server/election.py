import random, pprint
from typing import List, Dict

def count(votes : List[List[str]], options : List[str]):
    options  : Dict[str, List[List[str]]] = { key : list(filter(lambda v: v[-1] == key, votes)) for key in list(options) }
    votes = len(votes)
    all_participants = votes
    thrown_out = 0
    result = { "winner" : False
             , "rounds" : []
             }
    while result["winner"] == False:
        # Does a candidate have more than 50%?
        result["rounds"].append(options)
        winners = list(filter(lambda o: len(options[o]) >= 0.5*votes, list(options)))
        if len(winners) == 1:
            result["winner"] = winners[0]
            break
        elif len(winners) >= 2:
            result["winner"] = None
            break
        elif len(winners) == 0:
            # Is there only one candidate left?
            if len(list(options)) == 1:
                result["winner"] = options(list(options)[0])
                break
            elif len(list(options)) == 0:
                result["winner"] = None
                break
            else:
                # Drop worst candidate and find out who voters liked next best
                sorted_options = sorted(list(options), key=lambda o: len(options[o]))
                worst = sorted_options[-1]
                worsts_votes = options.pop(worst)
                options = { key : [list(filter(lambda a: a != worst, vote)) for vote in options[key]] for key in list(options)}
                options = { key : options[key] for key in list(options) if options[key] != []}
                sum_votes = sum([len(options[o]) for o in list(options)])
                thrown_out += (votes - sum_votes)
                votes = sum_votes
                continue

    result["thrown_out"] = thrown_out
    if result["thrown_out"]/all_participants > 0.5:
        result["winner"] = "NoneOfTheOtherOptions"
    elif len(result["winner"])/all_participants == 0.5 and (result["thrown_out"]/all_participants == 0.5):
        result["winner"] = None

    result["winner"] = "NoneOfTheOtherOptions" if (result["thrown_out"]/all_participants) > 0.5 else result["winner"]
    return result
