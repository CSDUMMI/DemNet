from election import count_votes
import random, os

random.seed( a=os.environ['SEED'] )

def generate_random_vote(options):
    vote = []
    for option in options:
        vote.append(options[ random.randint(0,len(options)-1) ])
    return vote

def load_sample_votes():
    sample_votes = open('sample_votes.txt').read().split('\n')
    sample_votes = list(map( lambda v: v.split(';'), sample_votes ))
    return sample_votes

sample_votes = load_sample_votes()

result = count_votes(sample_votes,len(sample_votes), ['A','B','C','D','E','F','G','H','I','J'])

print("\nResult:{}".format(result))
