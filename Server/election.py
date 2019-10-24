def count_votes( votes, participant_count, options ):
    ballot = map( lambda option : { 'option' : option, 'support' : [] }, options )
    winner = distribute_votes( votes, participant_count, list(ballot) )
    return { "ballot": winner, "participants" : participant_count, "options" : options }

def distribute_votes( votes, participant_count, ballot ):
    if len(ballot[0]['support'])/participant_count > 0.5 or len(ballot) <= 1:
        return ballot # Winner!
    else:
        # Distribute votes
        for option in ballot:
            option['support'] = option['support'] + list(filter(lambda v: v[-1] == option['option'], votes))

        # Eliminate another low ranking option
        # Sort by Support
        ballot = sorted(ballot, key = lambda option : len(option['support']), reverse=True)

        looser = ballot.pop()
        print(f"Eliminated {looser}\n\n")
        looser['support'] = list(map(lambda v: v[:-1], looser['support']))
        return distribute_votes(looser['support'], participant_count, ballot)
