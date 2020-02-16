import random, pprint
from typing import List, Dict

def count(votes : List[List[str]], options : List[str]):
    options = { key : list(filter(lambda v: v[-1] == key, votes)) for key in list(options) }
    votes = len(votes)
    all_participants = votes
    thrown_out = 0
    result = { "winner" : False
             , "rounds" : []
             }
    while result["winner"] == False:
        # Does a candidate have more than 50%?
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
                thrown_out += (votes - sum([len(options[o]) for o in list(options)]))
                votes = sum([len(o) for o in options])
                continue

    result["thrown_out"] = thrown_out
    result["winner"] = "NoneOfTheOtherOptions" if (result["thrown_out"]/all_participants) > 0.5 else result["winner"]
    return result

def test(n, repeat_for=10**3,seed="A"):
    random.seed("A")
    for i in range(repeat_for):
        options = ["A","B","C","D"]
        votes = [random.sample(options,k=random.randint(1,len(options))) for i in range(n)]
        result = count(votes,options)
        print(f"""{result["winner"]}
Options : {options}
Votes: {votes}
Thrown out: {(result["thrown_out"]/len(votes))*100}%
        """)
