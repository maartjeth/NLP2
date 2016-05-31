"""
Generate feature vocabularies

The script constructs counter that count the frequencies of
of all features. These can later be used to for example map 
features to their ids.

N.B. For these four features, generating vocabularies takes
5-6 minutes.
"""

# Test / dev
kind = "test"

# Number of pars
num_parts = 5

# Filename of the parse (formatted with (kind, part))
parse_fn = '../data-%s/parse/translations-part%s.parse'

# Where to store the tag vocabulary?
# Please give every feature a name (e.g. tag, bigram, article, preposition, ...)
tag_voc_fn = "../data-%s/ling-features/tag-vocabulary.pickle" % kind
bigram_voc_fn = "../data-%s/ling-features/bigram-vocabulary.pickle" % kind
art_voc_fn = "../data-%s/ling-features/article-vocabulary.pickle" % kind
prep_voc_fn = "../data-%s/ling-features/preposition-vocabulary.pickle" % kind

##############################################################

import cPickle as pickle
from collections import Counter

# A counter for every feature...
tags = Counter()
bigrams = Counter()
art_features = Counter()
prep_features = Counter()
# ... 

# All prepositions
preps = ['nach', 'gegen', 'an', 'hinter', 'neben', 'zwischen', 'vor', 
		'in', 'zu', 'entlang', 'ohne', 'auf', 'aus', 'ausser', 'mit', 
		'unter', 'bis', 'von', 'bei', 'seit', 'um', 'durch']
preps = dict([(prep, None) for prep in preps])

# All articles
articles = ['die', 'des', 'dem', 'den', 'der', 'das']
articles = dict([(art, None) for art in articles])

for part in range(1, num_parts + 1):
	print "Starting with part %s..." % part
	with open(parse_fn % (kind, part), 'r') as parsed_file:
		lines = []
		while True:

			# Read next line
			try:
				line = parsed_file.next()
			except StopIteration: 
				break

			# Collect all lines for this sentence
			if line != '\n':
				lines.append(line.replace("\n", "").split("\t"))
				continue
			
			# Else, process the sentence
			for word_id, word_form, _, lemma, _, \
				tag, _, morph, _, head, _, _, _, _ in lines:

				# All info about the head
				head_info = lines[int(head) - 1]

				# Tag features
				tags[tag] += 1

				# Bigram features
				head_tag = "ROOT" if head == 0 else head_info[5]
				bigram = (head_tag, tag)
				bigrams[bigram] += 1

				# Article features
				try:
					articles[word_form] # A sneaky way to test if something's in a dict
					art_features[(word_form, head_info[7])] += 1
				except KeyError: pass

				# Prepositions 
				# Note that this is a pretty rare feature?
				head_word = head_info[1]
				try:
					preps[head_word], articles[word_form]
					prep_features[ (head_word, morph[:3]) ] += 1
				except KeyError: pass

				# Add other features here
				# Or generate them in a different file;
				# you only want to run it once, after all.
				# ...
				
			lines = []

# # Store tag and bigram counters
with open(tag_voc_fn, 'wb') as file:
	pickle.dump(tags, file, pickle.HIGHEST_PROTOCOL)

with open(bigram_voc_fn, 'wb') as file:
	pickle.dump(bigrams, file, pickle.HIGHEST_PROTOCOL)

with open(art_voc_fn, 'wb') as file:
	pickle.dump(art_features, file, pickle.HIGHEST_PROTOCOL)

with open(prep_voc_fn, 'wb') as file:
	pickle.dump(prep_features, file, pickle.HIGHEST_PROTOCOL)


