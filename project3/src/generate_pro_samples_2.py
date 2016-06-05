"""
Generates random samples from the 1000best lists.

It writes the samples to a file, where every line contains the sample for the
corresponding sentence. By a sample we mean a list of line-numbers that identify
the candidates in the 1000best list. 

Since we are sampling pairs of candidates, every line will contain `2*sample_size` 
candidates, where every two successive candidates form a pair. So if you have 
`sample_size=2` and sample candidates `(3456, 3891)` and `(3921, 3210)` for 
sentence 3, the third line of the output file is exactly `3456,3891,3921,3210`.

Note that the candidates in every pair are always distinct.
"""
import json
import random
from Features import *
import numpy as np

# Size of the sample
sample_size = 1

#################################################################

# We don't need samples for test...
kind = "dev"

sample_size = 1000

top_n = 500;

# Filenames 
output_fn = "../data-{kind}/samples/{kind}-samples-{size}-separated-{top_n}.txt"
output_fn = output_fn.format(kind=kind, size=sample_size, top_n=top_n)
# output_fn = "../data-dev/samples/val-samples-%s-3.txt" 	% sample_size

# Load sentences data
sentences_fn = '../data-dev/dev-sentences.json'
sentences = json.load(open(sentences_fn, 'r'))

pro_scores_fn = "../data-{kind}/{kind}-meteor.txt".format(kind=kind)

# Construct samples
scores = Scores(pro_scores_fn, "", sentences)
output_file = open(output_fn, 'w')
for i, scores in enumerate(scores.iter_sentence_features()):
	# if i>1: break
	sentence = sentences[i]
	scores = np.array(scores).T
	sorted_scores = scores.argsort()
	best_candidates = sorted_scores[0, :top_n] + sentence['first_line']
	worst_candidates = sorted_scores[0, -top_n:] + sentence['first_line']

	sample = []
	for i in range(sample_size):
		sample.append(random.choice(best_candidates))
		sample.append(random.choice(worst_candidates))
	
	output_file.write(",".join(map(str, sample)) + "\n")

output_file.close()