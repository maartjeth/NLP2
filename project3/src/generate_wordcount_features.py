from Features import *
import json
import numpy as np
import re

kind = "test"

candidates_fn = "../data/nlp2-{kind}.1000best".format(kind=kind)

sentences_fn = "../data-{kind}/{kind}-sentences.json".format(kind=kind)
sentences = json.load(open(sentences_fn, 'r'))

wordcount_fn = "../data-{kind}/features/{kind}-wordcount-features.txt".format(kind=kind)

#######################################################

# Function that gets the wordcount from a list of lines
expr = re.compile(" \|\d+-\d+\| ")
def get_sentence_length(line):
	raw = line.split(" ||| ")[1]
	return len( expr.split(raw) )

# Iterate over all lines and dump wordcounts of all sentences
def_features = DefFeatures(candidates_fn, '', sentences)
wordcount_file = open(wordcount_fn, 'w')
for i, (_, lines) in enumerate(def_features.iter_sentences()):
	# if i>3: break
	if i % 100 == 0: print "  {i:>4} sentences done".format(i=i)

	# Get lengths
	lengths = np.array( map(get_sentence_length, lines), dtype="float" )
	
	# Normalize length
	minlen = lengths.min()
	maxlen = lengths.max()
	if maxlen == minlen:
		rel_lengths = np.ones(len(lines), dtype="int")
	else:
		rel_lengths = np.round( (lengths - minlen) / (maxlen - minlen), 4)
	
	# Write out!
	wordcount_file.write( "\n".join(map(str, rel_lengths)) + "\n")

wordcount_file.close()