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

    print(f"Votes:{votes}")
    print(f"Result:{count_votes(votes,len(votes),options)}")

if __name__ == '__main__':
    i = 10
    while(i > 0):
        generate_elections(['A','B','C','D'],random.randint(5,10))
        i -= 1
