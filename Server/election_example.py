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

def generate_election( options, participants ):
    votes = []
    result_file = open("sample_election.el","w")
    while( participants > 0 ):
        votes.append( generate_random_vote(options) )
        participants -= 1

    winner = count_votes( len(votes), votes, options, fs=result_file )




if __name__ == '__main__':
    i = 10
    while(i > 0):
        generate_election(['A','B','C','D', 'E', 'F', 'G', 'H', 'I'],random.randint(10**2,10**3))
        i -= 1
