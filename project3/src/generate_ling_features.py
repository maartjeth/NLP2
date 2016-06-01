"""
Generates linguistic features.

"""

kind = "test"
num_parts = 6

# Filename of the parse
#parse_fn = '../data-dev/parse/translations-part%s.parse'
parse_fn = '../output/translation.1.parse' # FOR TESTING!!!!!!

# Feature vocabularies (inputs)
tag_voc_fn = "../data-%s/ling-features/tag-vocabulary.pickle" % kind
bigram_voc_fn = "../data-%s/ling-features/bigram-vocabulary.pickle" % kind
art_voc_fn = "../data-%s/ling-features/article-vocabulary.pickle" % kind
prep_voc_fn = "../data-%s/ling-features/preposition-vocabulary.pickle" % kind
word_count_voc_fn = "../data-%s/ling-features/wordcount-vocabulary.pickle" % kind
es_voc_fn = "../data-%s/ling-features/es-vocabulary.pickle" % kind
art_pl_voc_fn = "../data-%s/ling-features/artpl-vocabulary.pickle" % kind
prep_art_voc_fn = "../data-%s/ling-features/prepart-vocabulary.pickle" % kind

# Files to store features in (outputs)
tag_features_fn = "../data-%s/ling-features/tag-features.txt" % kind
bigram_features_fn = "../data-%s/ling-features/bigram-features.txt" % kind
art_features_fn = "../data-%s/ling-features/art-features.txt" % kind
prep_features_fn = "../data-%s/ling-features/prep-features.txt" % kind
word_count_features_fn = "../data-%s/ling-features/wordcount-features.txt" % kind
es_features_fn = "../data-%s/ling-features/es-features.txt" % kind
art_pl_features_fn = "../data-%s/ling-features/artpl-features.txt" % kind
prep_art_features_fn = "../data-%s/ling-features/prepart-features.txt" % kind

##############################################################

import cPickle as pickle
from collections import Counter

def get_feature2id(feat_voc_fn):
	"""Get a feat2id dictionary, with no pruning!"""
	with open(feat_voc_fn, 'rb') as file:
		features = pickle.load(file)
	return dict([ (feat, i) for i, feat in enumerate(features.keys())])

def ids2str(lst):
	return ",".join(map(str, lst))

## Load the feature dictionaries and turn them into value2id 
# dictionaries Here you could also prune them for example: 
# counters have this handy Counter.most_common(n) method. For that,
# change the get_feature2id function.
tag2id = get_feature2id(tag_voc_fn)
bigram2id = get_feature2id(bigram_voc_fn)
art2id = get_feature2id(art_voc_fn)
prep2id = get_feature2id(prep_voc_fn)
wordcount2id = get_feature2id(word_count_voc_fn)
es2id = get_feature2id(es_voc_fn)
artpl2id = get_feature2id(art_pl_voc_fn)
prepart2id = get_feature2id(prep_art_voc_fn)

# To keep track of the sentence with the smallest number of words and the largest number
min_word_count = float("inf")
max_word_count = 0.0

for part in range(1, num_parts + 1):
	print "Starting with part %s..." % part

	# Open all files
	#parsed_file = open(parse_fn % part, 'r')
	parsed_file = open(parse_fn, 'r') # FOR TESTING!!!!!
	tag_features_file = open(tag_features_fn, 'w');
	bigram_features_file = open(bigram_features_fn, 'w');
	art_features_file = open(art_features_fn, 'w');
	prep_features_file = open(prep_features_fn, 'w');
	wordcount_features_file = open(word_count_features_fn, 'w');
	es_features_file = open(es_features_fn, 'w');
	art_pl_features_file = open(art_pl_features_fn, 'w');
	prep_art_features_file = open(prep_art_features_fn, 'w');

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
		tag_ids = []
		bigram_ids = []
		art_ids = []
		prep_ids = []
		wordcount_ids = []
		es_ids = []
		artpl_ids = []
		prepart_ids = []
		
		# Now loop through the candidate block and store the features
		# Note that this is very similar to when you generate the vocabularies
		# Note that every line represents one word

		total_sg = 0.0
		total_pl = 0.0
		total_masc = 0.0
		total_fem = 0.0
		total_neut = 0.0

		for word_id, word_form, _, lemma, _, \
			tag, _, morph, _, head, _, _, _, _ in lines:
			head_info = lines[int(head) - 1]

			if int(word_id) - 2 < 0:
				linear_head_info = ['ROOT', 'ROOT', 'ROOT', 'ROOT', 'ROOT', 'ROOT', 'ROOT', 'ROOT', 'ROOT', 'ROOT', 'ROOT', 'ROOT', 'ROOT', 'ROOT']
			else:
				linear_head_info = lines[int(word_id) - 2]

			# Tag ids
			try:
				tag_ids.append(tag2id[tag])
			except KeyError: pass
			
			# Bigram ids
			try:
				head_tag = "ROOT" if head == 0 else head_info[5]
				bigram_ids.append( bigram2id[(head_tag,tag)] )
			except KeyError: pass

			# Art ids
			try:
				art_ids.append(art2id[ (word_form, head_info[7]) ])
			except KeyError: pass
			
			# Prep ids
			try:
				head_word = head_info[1]
				prep_ids.append(prep2id[ (head_word, morph[:3]) ])
			except KeyError: pass

			# Word count ids

			# Count number of words in the sentence
			num_words_sent = len(lines)

			# Keep track of smallest and largest sent # perhaps you want all features between this value, or make ranges?
			if num_words_sent > max_word_count:
				max_word_count = num_words_sent
			if num_words_sent < min_word_count:
				min_word_count = num_words_sent

			try:
				wordcount_ids.append(wordcount2id[num_words_sent])
			except KeyError: pass

			# Es (as nominative) + word
			if word_form == 'es' and morph[:3] == 'nom':
				es_feature = ('es', head_info[1])
				try:
					es_ids.append(es2ids[es_feature])
				except KeyError: pass

			# eine / die + plural (to get at least a grasp on whether the plural goes well)
			if (word_form == 'eine' or word_form == 'die') and head_info[7][4:6] == 'pl':
				if head_info[1][-2:] == 'er' or head_info[1][-2:] == 'en':
					art_pl_feature = (word_form, head_info[1][-2:])
				elif head_info[1][-1:] == 'e' or head_info[1][-1:] == 'n' or head_info[1][-1:] == 'r' or head_info[1][-1:] == 's':
					art_pl_feature = (word_form, head_info[1][-1:])
				else:
					art_pl_feature = (word_form, 'NONE')

				try:
					artpl_ids.append(artpl2id[art_pl_feature])
				except KeyError: pass

			# prep + article that follows # TODO, not thorougly tested yet
			try:
				prepart_ids.append(prepart2id[word_form, linear_head_info[1]])
			except KeyError: pass
			
			# Ratio singular / plural nouns
			if 'sg' in morph:
				total_sg += 1
			if 'pl' in morph:
				total_pl += 1

			# ratio male/female/neuter
			if 'masc' in morph:
				total_masc += 1
			if 'fem' in morph: # TODO: check if it's really called fem
				total_fem += 1
			if 'neut' in morph:
				total_neut += 1

		ratio_sg_pl = float(total_sg / total_pl) # TODO: add these 4 lines as feature
		ratio_masc = float(total_masc / (total_fem + total_neut))
		ratio_fem = float(total_fem / (total_masc + total_neut))
		ratio_neut = float(total_neut / (total_masc + total_fem))

			

		# Remove duplicates and sort (cause, hey, why not?) # WHY ARE THERE DUPLICATES AT ALL?
		# 100% zeker dat we een vector per candidate hebben en niet per meer?
		bigram_ids = set(sorted(bigram_ids))
		tag_ids = set(sorted(tag_ids))
		art_ids = set(sorted(art_ids))
		prep_ids = set(sorted(prep_ids))
		wordcount_ids = set(sorted(wordcount_ids))
		es_ids = set(sorted(es_ids))
		artpl_ids = set(sorted(artpl_ids))
		prepart_ids = set(sorted(prepart_ids))
		
		# Write results
		tag_features_file.write(ids2str(tag_ids) + "\n")
		bigram_features_file.write(ids2str(bigram_ids) + "\n")
		art_features_file.write(ids2str(art_ids) + "\n")
		prep_features_file.write(ids2str(prep_ids) + "\n")
		wordcount_features_file.write(ids2str(wordcount_ids) + "\n")
		es_features_file.write(ids2str(es_ids) + "\n")
		art_pl_features_file.write(ids2str(artpl_ids) + "\n")
		prep_art_features_file.write(ids2str(prepart_ids) + "\n")
		
		# reset
		lines = []

	# Close open files
	parsed_file.close()
	tag_features_file.close()
	bigram_features_file.close()
	art_features_file.close()
	prep_features_file.close()
	wordcount_features_file.close()
	es_features_file.close()
	art_pl_features_file.close()
	prep_art_features_file.close()


