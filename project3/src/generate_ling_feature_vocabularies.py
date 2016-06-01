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
#parse_fn = '../data-%s/parse/translations-part%s.parse'
parse_fn = '../output/translation.1.parse' # FOR TESTING!!!!!!

# Where to store the tag vocabulary?
# Please give every feature a name (e.g. tag, bigram, article, preposition, ...)
tag_voc_fn = "../data-%s/ling-features/tag-vocabulary.pickle" % kind
bigram_voc_fn = "../data-%s/ling-features/bigram-vocabulary.pickle" % kind
art_voc_fn = "../data-%s/ling-features/article-vocabulary.pickle" % kind
prep_voc_fn = "../data-%s/ling-features/preposition-vocabulary.pickle" % kind
word_count_voc_fn = "../data-%s/ling-features/wordcount-vocabulary.pickle" % kind
es_voc_fn = "../data-%s/ling-features/es-vocabulary.pickle" % kind
art_pl_voc_fn = "../data-%s/ling-features/artpl-vocabulary.pickle" % kind
prep_art_voc_fn = "../data-%s/ling-features/prepart-vocabulary.pickle" % kind

##############################################################

import cPickle as pickle
from collections import Counter

# A counter for every feature...
tags = Counter()
bigrams = Counter()
art_features = Counter()
prep_features = Counter()
word_count_features = Counter()
es_features = Counter()
art_pl_features = Counter()
prep_art_features = Counter()
# ... 

# All prepositions TODO: add the non ascii characters!!!
preps = ['nach', 'gegen', 'an', 'hinter', 'neben', 'zwischen', 'vor', 
		'in', 'zu', 'entlang', 'ohne', 'auf', 'aus', 'ausser', 'mit', 
		'unter', 'bis', 'von', 'bei', 'seit', 'um', 'durch']
preps = dict([(prep, None) for prep in preps])

# All articles
articles = ['die', 'des', 'dem', 'den', 'der', 'das']
articles = dict([(art, None) for art in articles])

# To keep track of the sentence with the smallest number of words and the largest number
min_word_count = float("inf")
max_word_count = 0

for part in range(1, num_parts + 1):
	print "Starting with part %s..." % part
	#with open(parse_fn % (kind, part), 'r') as parsed_file:
	with open(parse_fn, 'r') as parsed_file:  # FOR TESTING!!!!!!
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

				# word before, not dependency wise
				if int(word_id) - 2 < 0:
					linear_head_info = ['ROOT', 'ROOT', 'ROOT', 'ROOT', 'ROOT', 'ROOT', 'ROOT', 'ROOT', 'ROOT', 'ROOT', 'ROOT', 'ROOT', 'ROOT', 'ROOT']
				else:
					linear_head_info = lines[int(word_id) - 2]				

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

				# Count number of words in the sentence
				num_words_sent = len(lines)

				# Keep track of smallest and largest sent
				if num_words_sent > max_word_count:
					max_word_count = num_words_sent
				if num_words_sent < min_word_count:
					min_word_count = num_words_sent

				word_count_features[num_words_sent] += 1
				
				# Es (as nominative) + word
				if word_form == 'es' and morph[:3] == 'nom':
					es_feature = ('es', head_info[1])
					es_features[es_feature] += 1

				# eine / die + plural (to get at least a grasp on whether the plural goes well)
				if (word_form == 'eine' or word_form == 'die') and head_info[7][4:6] == 'pl':
					if head_info[1][-2:] == 'er' or head_info[1][-2:] == 'en':
						art_pl_feature = (word_form, head_info[1][-2:])
					elif head_info[1][-1:] == 'e' or head_info[1][-1:] == 'n' or head_info[1][-1:] == 'r' or head_info[1][-1:] == 's':
						art_pl_feature = (word_form, head_info[1][-1:])
					else:
						art_pl_feature = (word_form, 'NONE')

					art_pl_features[art_pl_feature] += 1

				# prep + article that follows # TODO, not thorougly tested yet
				try:
					preps[word_form], articles[linear_head_info[1]]
					prep_art_features[(word_form, linear_head_info[1])] += 1
				except KeyError: pass

				# Ratio singular / plural nouns
				# ratio male/female/neuter
	


				#if (word_form )	
				# Add other features here
				# Or generate them in a different file;
				# you only wantto run it once, after all.
				# ...
				
				# word count sentences --> note that the sentences have many different lenghts, so does this work --> perhaps feature like small/large

				# ratio singular / plural nouns

				# es (as nominative) + word --> often this seems to be a thing as well, many options

				# ratio male/female/neuter --> if you don't know you may at least decide based on common knowledge ---> only female words are unlikely, as well as only male words..

				# eine bezahlbare Technologien / eine bezahlbare Technologie --> eine (plural/singular) + laatste letter noun die erop volgt?

				# prep + article that follows (literate translation as we cannot rely on the parser) # see sentence untitled file

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

with open(word_count_voc_fn, 'wb') as file:
	pickle.dump(word_count_features, file, pickle.HIGHEST_PROTOCOL)

with open(es_voc_fn, 'wb') as file:
	pickle.dump(es_features, file, pickle.HIGHEST_PROTOCOL)

with open(art_pl_voc_fn, 'wb') as file:
	pickle.dump(art_pl_features, file, pickle.HIGHEST_PROTOCOL)

with open(prep_art_voc_fn, 'wb') as file:
	pickle.dump(prep_art_features, file, pickle.HIGHEST_PROTOCOL)

