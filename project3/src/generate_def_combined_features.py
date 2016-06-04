from Features import *
import json
from sklearn.preprocessing import PolynomialFeatures
import numpy as np


kind = "test"

degree = 2

candidates_fn = "../data/nlp2-{kind}.1000best".format(kind=kind)

sentences_fn = "../data-{kind}/{kind}-sentences.json".format(kind=kind)
sentences = json.load(open(sentences_fn, 'r'))

combined_fn = "../data-{kind}/features/{kind}-def-combined-{degree}-features.txt"
combined_fn = combined_fn.format(kind=kind, degree=degree)

#######################################################

polyfeat = PolynomialFeatures(degree)
def_features = DefFeatures(candidates_fn, '', sentences)
combined_file = open(combined_fn, 'w')
for i, features in enumerate(def_features.iter()):
	# if i>20000: break
	if i % 5000 == 0: print "  {i:>6} candidates done".format(i=i)

	features = polyfeat.fit_transform([features])[0]
	features = np.round(features, 5)
	combined_file.write( ",".join(map(str, features)) + "\n" )

combined_file.close()