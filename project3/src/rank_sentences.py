import numpy as np
from sklearn.externals import joblib
from Features import *
import re


# Sample size in the PRO
sample_size = "100"

name = "val-meteor"

##############################################################

# Again, we don't need instances for the test set
kind = "val"

# Model
model_fn = '../data-%s/models/%s-classifier-%s.skl-pickle' % (kind, name, sample_size)

# File with 1000best training instances
candidates_fn = "../data/nlp2-dev.1000best"# % kind

# Sentences information
sentences_fn = '../data-dev/dev-sentences.json'
sentences = json.load(open(sentences_fn,'r'))

## For validation:
val_sentences = json.load(open('../data-dev/val-sentences.json','r'))
val_sentences = [s['sentence'] for s in val_sentences]


sentence_ranking_fn = "../data-%s/results/%s-sentence-ranking-%s.txt" % (kind, name, sample_size)
best_translations_fn = "../data-%s/results/%s-best-translations-%s.txt" % (kind, name, sample_size)
targets_fn = "../data-%s/results/%s-best-translations-targets-%s.txt" % (kind, name, sample_size)

# Load model
model = joblib.load(model_fn)
weights = model.coef_
	
def ids2str(lst):
	return ",".join(map(str, lst))

######### FEATURE OBJECTS ################################
def_features = DefFeatures(candidates_fn, '', sentences)
all_features = [def_features] 

sentence_ranking_file = open(sentence_ranking_fn, 'w')
best_translations_file = open(best_translations_fn, 'w')
targets_file = open(targets_fn, 'w')

for i, (sentence, features, lines) in enumerate(def_features.iter_sentences()):
	# if i>=2: break
	if i not in val_sentences: continue

	if i % 100 == 0: print "Done with sentence %s" % i

	# Calculate the scores of the sentence
	scores = weights.dot(np.array(features).T)[0]
	
	# Get the ranking.
	# Note that argsort returns the lowest score first
	ranking = np.argsort(scores)#[::-1]
	sentence_ranking_file.write(ids2str(ranking) + "\n")
	
	# Extract the best translation
	best = lines[ranking[0]]
	parts = re.split(" \|\d+-\d+\| ", best.split(" ||| ")[1])
	translation = " ".join(parts)
	best_translations_file.write(translation + "\n")
	
	# Write out targets as well
	targets_file.write(sentence['target'].encode('utf-8')+"\n")

sentence_ranking_file.close()
best_translations_file.close()
targets_file.close()

