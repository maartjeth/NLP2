"""
Generates linguistic features.

"""

kind = "dev"
num_parts = 6

# Which features should be calculated?
USED_FEATURES ='tag bigram prep es artpl prepart'
USED_FEATURES = dict([(f, None) for f in USED_FEATURES.split()])

# Filename of the parses
parse_fn = '../data-{kind}/parse/translations-part{part}.parse'

# Filename template for feature vocabularies (input)
# Always use the same vocabularies: those from the dev set!
feature_voc_fn = "../data-dev/features/dev-{feature}-vocabulary.pickle"


##############################################################

import cPickle as pickle
from collections import Counter
from feature_extractors import *

# Load all feature files and feature vocabularies
COUNTERS = dict([(feat, Counter()) for feat in USED_FEATURES])

# All prepositions
with open('prep.txt', 'r') as preps_f:
	all_preps = preps_f.readline().split(" ")
	all_preps = list(all_preps)
	preps = dict([(prep, None) for prep in all_preps])

# All articles
articles = ['die', 'des', 'dem', 'den', 'der', 'das']
articles = dict([(art, None) for art in articles])

##############################################################

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
	
		# Now loop through the candidate block and store the features
		# Note that this is very similar to when you generate the vocabularies
		# Note that every line represents one word
		for word_id, word, _, lemma, _, tag, _, morph, _, head, _, _, _, _ in lines:
			
			# Parse information of the head
			head_id, head_word, _, _, _, head_tag, _, head_morph, _, _, _, _, _, _ = lines[int(head) - 1]
			head_tag = "ROOT" if head == 0 else head_tag

			## POS-TAG FEATURES
			try: 
				USED_FEATURES['tag']
				COUNTERS['tag'][tag] += 1
			except KeyError: pass
			
			# BIGRAM FEATURES
			try: 
				USED_FEATURES['bigram']
				COUNTERS['bigram'][ (head_tag, tag) ] += 1
			except KeyError: pass

			## PREPOSITION FEATURES
			# Consists of (preposition, case) pairs
			try:
				USED_FEATURES['prep']
				# Is this an article with preposition as head?
				preps[head_word], articles[word] 
				feature = get_prep_feature(morph, head_word)
				COUNTERS['prep'][feature] += 1
			except KeyError: pass

			# Es (as nominative) + word
			try:
				USED_FEATURES['es']
				feature = get_es_feature(word, morph, head_word)
				if feature: COUNTERS['es'][feature] += 1
			except KeyError: pass

			## ARTICLE + PLURAL
			# eine / die + plural (to get at least a grasp on whether the plural goes well)
			# The head is tagged as plural, but is it? Check the head word ending.
			try:
				USED_FEATURES['artpl']
				feature = get_eine_feature(word, head_word, head_morph)
				if feature: COUNTERS['artpl'][feature] += 1
			except KeyError: pass

			## PREPART 
			# prep + article that follows 
			try:
				USED_FEATURES['prepart']
				try:
					# Word ids are 1-based, so the next index is the current word_id
					next_word = lines[ int(word_id) ][1]
				except IndexError: pass

				preps[word], articles[next_word]
				COUNTERS['prepart'][ (word, next_word) ] += 1
			except KeyError: pass
	
		# reset
		lines = []

# Dump all feature vocabularies
for feature, counter in COUNTERS.items():
	fn = feature_voc_fn.format(feature=feature)
	with open(fn, 'wb') as file:
		pickle.dump(counter, file, pickle.HIGHEST_PROTOCOL) 


