import functools

def count_votes( votes, participant_count, options ):
    ballot = map( lambda option : { 'option' : option, 'support' : [] }, options )
    winner = distribute_votes( votes, participant_count, list(ballot) )
    return { "ballot": winner, "participants" : participant_count, "options" : options }

def distribute_votes( votes, participant_count, ballot ):
    if len(ballot[0]['support']) > participant_count * 0.5 or len(ballot) <= 1:
        return ballot # Winner!
    else:
        # Distribute votes
        for option in ballot:
            option['support'] = option['support'] + list(filter(lambda v: v[-1] == option['option'], votes))

        # Eliminate another low ranking option
        # Sort by Support
        ballot = sorted(ballot, key = lambda option : len(option['support']), reverse=True)

        looser = least_popular(ballot)
        ballot.remove(looser)
        print(f"Eliminated {looser}\n\n")
        looser['support'] = list(map(lambda v: v[:-1], looser['support']))
        return distribute_votes(looser['support'], participant_count, ballot)

def least_popular( ballot ):
    # If there is a tie, look at the option, that is more popular in the alternative votes.
    if len(ballot[-1]['support']) == len(ballot[-2]['support']):
        option1 = ballot[-1]
        option2 = ballot[-2]
        alternative_votes = list( map( lambda option: option['support'][:-1], ballot ) )
        alternative_votes = functools.reduce( lambda x, y : x + y, alternative_votes )

        print(f"TIE: between {option1['option']} and {option2['option']}")
        print(f"{option1['option']}: {len(option1['support'])}")
        print(f"{option1['support']}")
        print(f"{option2['option']}: {len(option2['support'])}")
        print(f"{option2['support']}")

        print(f"Alternative Votes:{ alternative_votes}")

        i = -1
        least_popular = False

        while(not least_popular):
            is_tie = alternative_votes[i].count(option1['option']) - alternative_votes.count(option2['option'])

            if is_tie < 0:
                least_popular = option1
            elif is_tie > 0:
                least_popular = option2
            else:
                least_popular = False
        return least_popular
    else:
        return ballot[-1]
