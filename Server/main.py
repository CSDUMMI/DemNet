import json

def count_votes( votes, particpant_count, options ):
    ballot = map( lambda option : { "option" : option, "support" : list() }, options )
    return _count_votes( votes, particpant_count, list(ballot) )

def _count_votes( votes, particpant_count, ballot ):
    # Base case
    if len(ballot) == 1:
        return ballot[0]

    # Sort the votes to their first choice
    for option in ballot:
        option["support"] = option["support"] + list(
                            filter(
                            lambda v: v[ len(v)-1] == option["option"], votes
                            )
                            )
    ballot = sorted( ballot, key=lambda option: len(option["support"]), reverse=True )
    # If any option got more than 50% of the support, that is the winner.
    if len( ballot[0]['support'] ) > particpant_count*0.5 or len(ballot) == 0:
        return ballot[0]
    else:
        # Eliminate least popular option and recount those results
        looser = ballot.pop()
        print(f"Looser: {looser['option']} " )
        looser = list(map( lambda v: v[:-1], looser['support']))

        print( looser )
        return _count_votes( looser, particpant_count, ballot )
# Expected Winner = C
votes = [
            [ 'A', 'B', 'C' ],
            [ 'B', 'C', 'A' ],
            [ 'C', 'B', 'A' ],
            [ 'A', 'B', 'C' ],
            [ 'A', 'C', 'B' ],
            [ 'B', 'A', 'C' ]
        ]

print ( count_votes( votes, len( votes ), [ 'A', 'B', 'C' ] ) )
