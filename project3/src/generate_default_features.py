from Features import *
import json
import numpy as np


kind = "test"

candidates_fn = "../data/nlp2-{kind}.1000best".format(kind=kind)

sentences_fn = "../data-{kind}/{kind}-sentences.json".format(kind=kind)
sentences = json.load(open(sentences_fn, 'r'))

def_features_fn = "../data-{kind}/features/{kind}-def-features.txt".format(kind=kind)

#######################################################

def_features = DefFeatures(candidates_fn, '', sentences)
def_features_file = open(def_features_fn, 'w')
for i, features in enumerate(def_features.iter()):
	# if i>2: break
	if i % 5000 == 0: print "  {i:>6} candidates done".format(i=i)
	
	def_features_file.write( ",".join(map(str, features)) + "\n" )

def_features_file.close()