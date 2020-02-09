import election
import random, os, json

random.seed(os.environ["SEED"])

"""Utility function to easily create new election ballots, if necessary
"""
def generate_ballot():
    options_population = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    options = random.choices(
                options_population
                , k=random.randint(1,len(options_population))
                )

    votes = [random.sample(options,random.randint(1,len(options))) for i in range(random.randint(10,100))]

    participants = random.randint(len(votes), len(votes)+10)
    return (votes,participants,options)

def test_count_votes():
    # Random ballot test cases
    for i in range(100):
        ballot = generate_ballot()
        test_file = open("test_election.el","w")
        result = election.count_votes(ballot[0],ballot[1],ballot[2],fs=test_file)

        assert test_file.closed

        election_log = open("test_election.el","r").read()

        # Format checks in the log:

        # Votes, Thrown and Winner fields must exist
        assert election_log.startswith("Votes:\n")
        (votes,_,rest) = election_log.partition("\nThrown:\n")
        (thrown,_,winner) = election_log.partition("\nWinner:\n")
        (_,_,votes) = votes.partition("Votes:\n")
        votes = json.loads(votes)
        assert winner.strip() == str(result)

    # Testing on one special ballot
    options = ["A","B","C"]
    votes = [["A","B","C"],["A","C","B"],["A","C","B"]]
    participants = len(votes)
    assert ("B", 2/3) == election.count_votes(votes,participants,options)


    participants = 10
    assert ("NoneOfTheOtherOptions", 8) == election.count_votes(votes,participants,options)
