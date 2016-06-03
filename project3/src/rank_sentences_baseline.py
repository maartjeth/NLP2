import numpy as np
from sklearn.externals import joblib
from Features import *
import re
model_fn = '../data-dev/models/defdata-classifier-100.skl-pickle'


# Sample size in the PRO
name = "baseline"

##############################################################

# Again, we don't need instances for the test set
kind = "test"

# File with 1000best training instances
candidates_fn = "../data/nlp2-%s.1000best" % kind

# Sentences information
sentences_fn = '../data-%s/%s-sentences.json' % (kind, kind)
sentences = json.load(open(sentences_fn,'r'))

sentence_ranking_fn = "../data-test/results/%s-sentence-ranking.txt" % (name)
best_translations_fn = "../data-test/results/%s-best-translations.txt" % (name)

# Load baseline weights
with open('../data/baseline.weights', 'r') as file:
	weights = []
	for feature in file.read().split("\n"):
		if feature == "": continue
		parts = re.split("\s?([A-Za-z0-9]+)=\s?", feature)[1:]
		if parts[0] == "InputFeature0": continue
		weights += map(float, parts[1].split(" "))
	weights = np.array(weights)

def ids2str(lst):
	return ",".join(map(str, lst))

######### FEATURE OBJECTS ################################
def_features = DefFeatures(candidates_fn, '', sentences)

sentence_ranking_file = open(sentence_ranking_fn, 'w')
best_translations_file = open(best_translations_fn, 'w')

for i, (features) in enumerate(def_features.iter_sentences()):
	# if i>=2: break
	# 
	if i % 100 == 0: print "Done with sentence %s" % i
	sentence = sentences[i]

	# Calculate the scores of the sentence
	scores = weights.dot(np.array(features).T)

	# Get the ranking.
	# Note that argsort returns the lowest score first
	ranking = np.argsort(scores)#[::-1]
	sentence_ranking_file.write(ids2str(ranking) + "\n")
	
	# Extract the best translation
	# best = lines[ranking[0]]
	# parts = re.split(" \|\d+-\d+\| ", best.split(" ||| ")[1])
	# translation = " ".join(parts)
	# best_translations_file.write(translation + "\n")
	
	
sentence_ranking_file.close()
best_translations_file.close()

