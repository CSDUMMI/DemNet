from election import count_votes
import random, os

random.seed( a=os.environ['SEED'] )

def generate_random_vote(options):
    vote = random.sample( options, k = len(options) )
    return vote

def load_sample_votes():
    sample_votes = open('sample_votes.txt').read().split('\n')
    sample_votes = list(map( lambda v: v.split(';'), sample_votes ))
    return sample_votes

def generate_elections( options, participants ):
    votes = []
    while( participants > 0 ):
        votes.append( generate_random_vote(options) )
        participants -= 1

    winner = count_votes( votes, len(votes), options )

    winners = []
    for i in range(len(options)):
        votes_in_i = list(map( lambda vote: vote[-i],votes ))
        winner_votes = votes_in_i.count(winner['ballot']['option'])
        winners.append( ( winner_votes, len(votes_in_i) ))

    print(f"Result:{winner['ballot']['option']}")

    for i in range(len(winners)):
        percentage = round((winners[i][0]/winners[i][1]) * 100, ndigits=2)
        print(f"Winner' votes in Vote #{i}:\t{winners[i][0]} of {winners[i][1]},\t{ percentage }% ")

if __name__ == '__main__':
    i = 10
    while(i > 0):
        generate_elections(['A','B','C','D', 'E', 'F', 'G', 'H', 'I'],random.randint(10**2,10**3))
        i -= 1
