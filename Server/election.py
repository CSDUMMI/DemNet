def count_votes( votes, participant_count, options ):
    ballot = map( lambda option : { "option" : option, "support" : list() }, options )
    return _count_votes( votes, participant_count, list(ballot) )


def _count_votes( votes, participant_count, ballot ):
    # Base case
    if len(ballot) == 1:
        return ballot

    # Sort the votes to their first choice
    for option in ballot:
        option["support"] = option["support"] + list(
                            filter(
                            lambda v: v[-1] == option["option"], votes
                            )
                            )

    ballot = sorted( ballot, key=lambda option: len(option["support"]), reverse=True )

    # Eliminate least popular option and recount those results, but
    # don't eliminate the NoneOfTheOtherOptions option, ever.
    if ballot[-1]['option'] == 'NoneOfTheOtherOptions':
        print('NoneOfTheOtherOptions didn\'t lose again')
        looser = ballot.pop( -2 ) # pop the one after 'NoneOfTheOtherOptions'
    else:
        looser = ballot.pop()

    print(f"Looser: {looser['option']} " )
    looser = list(map( lambda v: v[:-1], looser['support']))

    print( looser )
    return _count_votes( looser, participant_count, ballot )
