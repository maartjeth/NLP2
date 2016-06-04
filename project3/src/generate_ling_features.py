"""
Generates linguistic features.

"""

kind = "test"

num_parts = 5

# Which features should be calculated?
USED_FEATURES = 'tag bigram prep es artpl prepart ratios art'
USED_FEATURES = dict([(f, None) for f in USED_FEATURES.split()])

# Filename of the parses
parse_fn = '../data-{kind}/parse/translations-part{part}.parse'

# Filename template for feature vocabularies (input)
# Always use the same vocabularies: those from the dev set!
feature_voc_fn = "../data-dev/features/dev-{feature}-vocabulary.pickle"

# Filename template for feature files (output)
feature_fn = "../data-{kind}/features/{kind}-{feature}-features.txt"

##############################################################

import cPickle as pickle
from collections import Counter
from feature_extractors import *
import numpy as np

def get_feature2id(feature):
	"""Get a FEAT2ID dictionary, with no pruning!"""
	fn = feature_voc_fn.format(feature=feature)
	with open(fn, 'rb') as file:
		features = pickle.load(file)
	return dict([ (feat, i) for i, feat in enumerate(features.keys())])

def ids2str(lst):
	return ",".join(map(str, lst))

def open_feature_file(feature, kind=kind, how="w"):
	fn = feature_fn.format(kind=kind, feature=feature)
	return open(fn, how)

def get_ratios(parts):
	ratios = []
	for part in parts:
		try:
			ratios.append( part / sum(parts) )
		except ZeroDivisionError:
			ratios.append(0)
	return ratios

##############################################################

# Load all feature files and feature vocabularies
FEAT2ID = {}
FILES = {}
for feature in USED_FEATURES:
	FILES[feature] = open_feature_file(feature)
	try:
		FEAT2ID[feature] = get_feature2id(feature)
	except IOError: pass

# To keep track of the sentence with the smallest number of words and the largest number
min_word_count = float("inf")
max_word_count = 0.0

# All articles
articles = ['die', 'des', 'dem', 'den', 'der', 'das']
articles = dict([(art, None) for art in articles])

for part in range(1, num_parts + 1):
	print "Starting with part %s..." % part

	# Open the parse
	parsed_file = open(parse_fn.format(kind=kind, part=part), 'r')
	lines, i = [], 0
	while True:
		i += 1
		# if i > 500000: break
		
		# Read next line
		try: line = parsed_file.next()
		except StopIteration: break

		# Collect all lines for this sentence
		if line != '\n':
			lines.append(line.replace("\n", "").split("\t"))
			continue
		
		# A dictionary with ids for all sparse features
		feat_ids = {}
		for feat in USED_FEATURES:
			feat_ids[feat] = []

		total_sg = 0.0
		total_pl = 0.0
		total_masc = 0.0
		total_fem = 0.0
		total_neut = 0.0

		art_features = []

		# Now loop through the candidate block and store the features
		# Note that this is very similar to when you generate the vocabularies
		# Note that every line represents one word
		for word_id, word, _, lemma, _, tag, _, morph, _, head, _, _, _, _ in lines:
			head_id, head_word, _, _, _, head_tag, _, head_morph, _, _, _, _, _, _ = lines[int(head) - 1]
			head_tag = "ROOT" if head == 0 else head_tag

			## POS-TAG FEATURES
			try:
				USED_FEATURES['tag']
				feat_id = FEAT2ID['tag'][tag]
				feat_ids['tag'].append(feat_id)
			except KeyError: pass
			
			# BIGRAM FEATURES
			try:
				USED_FEATURES['bigram']
				feat_id = FEAT2ID['bigram'][ (head_tag, tag) ]
				feat_ids['bigram'].append(feat_id)
			except KeyError: pass

			## PREPOSITION FEATURES
			# Consists of (preposition, case) pairs
			try:
				USED_FEATURES['prep']
				feature = get_prep_feature(morph, head_word)
				feat_id = FEAT2ID['prep'][feature]
				feat_ids['prep'].append(feat_id)
			except KeyError: pass


			# Es (as nominative) + word
			try:
				USED_FEATURES['es']
				feature = get_es_feature(word, morph, head_word)
				feat_id = FEAT2ID['es'][feature]
				feat_ids['es'].append(feat_id)
			except KeyError: pass

			## ARTICLE + PLURAL 
			# eine / die + plural (to get at least a grasp on whether the plural goes well)
			try:
				USED_FEATURES['artpl']
				feature = get_eine_feature(word, head_word, head_morph)
				feat_id = FEAT2ID['artpl'][feature]
				feat_ids['artpl'].append(feat_id)
			except KeyError: pass

			## PREP + ART 
			# prep + article that follows 
			try:
				USED_FEATURES['prepart']
				try:
					next_word = lines[ int(word_id) ][1]
				except IndexError: pass

				feat_id = FEAT2ID['prepart'][ (word, next_word) ]
				feat_ids['prepart'].append(feat_id)
			except KeyError: pass
			
			## ARTICLE FEATURES:
			try: 
				USED_FEATURES['art']
				articles[word] # Is the word an article?
				art_features.append( get_art_feature(morph, head_morph) )
			except KeyError: pass

			# Ratio singular / plural and gender stuff
			total_sg 	+= 'sg' in morph
			total_pl 	+= 'pl' in morph
			total_masc 	+= 'masc' in morph
			total_fem 	+= 'fem' in morph
			total_neut 	+= 'neut' in morph
		
		# Remove duplicates and sort (cause, hey, why not?)
		for feature, ids in feat_ids.items():
			feat_ids[feature] = list(set(sorted(ids)))

		try:
			USED_FEATURES['art']
			if len(art_features) > 0:
				art_features = list(np.array(art_features).mean(axis=0))
			else:
				art_features = [1.0,1.0,1.0]
			feat_ids['art'] = art_features
		except KeyError: pass

		# Ratios: not a sparse feature, but we can pretend it is.
		try:
			USED_FEATURES['ratios']
			ratios = get_ratios([total_pl, total_sg])
			ratios += get_ratios([total_masc, total_fem, total_neut])
			feat_ids['ratios'] = ratios
		except KeyError: pass

		# Write results
		for feature, file in FILES.items():
			ids = ids2str(feat_ids[feature])
			file.write( ids + "\n")
		
		# reset
		lines = []

# Close open files
for file in FILES.values():
	file.close()
