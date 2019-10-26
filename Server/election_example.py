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
    winner_in_first = list(map( lambda vote: vote[-1],votes )).count(winner['option'])

    print(f"Result:{winner}")
    print(f"Winner occured in first election {winner_in_first} times")

if __name__ == '__main__':
    i = 10
    while(i > 0):
        generate_elections(['A','B','C','D'],random.randint(5,10))
        i -= 1
