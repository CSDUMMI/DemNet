from election import count_votes

def load_sample_votes():
    sample_votes = open('sample_votes.txt').read().split('\n')
    sample_votes = list(map( lambda v: v.split(';'), sample_votes ))
    return sample_votes

sample_votes = load_sample_votes()
print(count_votes(sample_votes,len(sample_votes), ['A','B','C','D','E','F','G','H','I','J']))
