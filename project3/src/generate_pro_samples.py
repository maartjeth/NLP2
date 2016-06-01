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

# Size of the sample
sample_size = 100

#################################################################

# We don't need samples for test...
kind = "dev"

# Filenames 
output_fn = "../data-%s/samples/%s-samples-%s.txt" % (kind,kind,sample_size)
sentences_fn = '../data-dev/dev-sentences.json' #% (kind,kind)

# Load sentences data
sentences = json.load(open(sentences_fn, 'r'))

## For validation:
# val_sentences = json.load(open('../data-val/val-sentences.json','r'))
# val_sentences = [s['sentence'] for s in val_sentences]

# # Construct samples
# # samples = []
with open(output_fn, 'w') as output_file:
	for sentence in sentences:

		## For validation:
		# if sentence['sentence'] in val_sentences:
		# 	output_file.write("\n")
		# 	continue

		# Now sample pairs of candidates (so that they are always distinct)
		sample = []
		lines = range(sentence['first_line'], sentence['last_line']+1)
		for i in range(sample_size):
			sample += random.sample(lines, 2)

		output_file.write(",".join(map(str, sample)) + "\n")

