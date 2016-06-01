"""
Post-process a ranking file.
"""

name = "defdata"
sample_size = "100"

sentence_ranking_fn = "../data-test/results/%s-sentence-ranking-%s.txt" % (name, sample_size)

candidates_fn = "../data/nlp2-%s.1000best" % kind
def_features = DefFeatures(candidates_fn, '', sentences)

with open(sentence_ranking_fn, 'r') as ranking_file:
	for i, line in enumerate(ranking_file):
		if i>5: break
		print line.replace("\n","").split(",")[0]