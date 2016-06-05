from Features import *
import json
import numpy as np
import re
import random

kind = "test"

degree = 2

candidates_fn = "../data/nlp2-{kind}.1000best".format(kind=kind)

sentences_fn = "../data-{kind}/{kind}-sentences.json".format(kind=kind)
sentences = json.load(open(sentences_fn, 'r'))

# val_sentences = json.load(open('../data-dev/val-sentences.json','r'))
# val_sentence_nrs = [s['sentence'] for s in val_sentences]

baseline_fn = "../models/baseline/test-baseline-translations-random.txt"

#######################################################

lines_iterator = DefFeatures(candidates_fn, '', sentences)
baseline_file = open(baseline_fn, 'w')

# Load baseline weights
# with open('../data/baseline.weights', 'r') as file:
# 	weights = []
# 	for feature in file.read().split("\n"):
# 		if feature == "": continue
# 		parts = re.split("\s?([A-Za-z0-9]+)=\s?", feature)[1:]
# 		if parts[0] == "InputFeature0": continue
# 		weights += map(float, parts[1].split(" "))
# 	weights = np.array(weights)

# def_features = DenseFeatures('../data-dev/features/dev-def-features.txt', '', sentences)
# for i, feat in enumerate(def_features.iter()):
# 	if i>5: break
# 	print weights.dot(feat)

translation_expr = re.compile(" \|\d+-\d+\| ")
for i, lines in enumerate(lines_iterator.iter_sentence_lines()):
	# if i>5: break
	# if i not in val_sentence_nrs: continue
	index = random.randint(0,len(lines)-1)
	split_lines = map( lambda line: line.replace("\n","").split(" ||| "), lines)
	words = translation_expr.split(split_lines[index][1])
	translation = " ".join(words)
	# print translation

	baseline_file.write(translation + "\n")

baseline_file.close()
