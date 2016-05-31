"""
Generates linguistic features.

"""

kind = "dev"
num_parts = 6

# Filename of the parse
parse_fn = '../data-%s/parse/translations-part%s.parse'

# Feature vocabularies (inputs)
tag_voc_fn = "../data-%s/ling-features/tag-vocabulary.pickle" % kind
bigram_voc_fn = "../data-%s/ling-features/bigram-vocabulary.pickle" % kind
art_voc_fn = "../data-%s/ling-features/article-vocabulary.pickle" % kind
prep_voc_fn = "../data-%s/ling-features/preposition-vocabulary.pickle" % kind

# Files to store features in (outputs)
tag_features_fn = "../data-%s/ling-features/tag-features.txt" % kind
bigram_features_fn = "../data-%s/ling-features/bigram-features.txt" % kind
art_features_fn = "../data-%s/ling-features/art-features.txt" % kind
prep_features_fn = "../data-%s/ling-features/prep-features.txt" % kind

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

for part in range(1, num_parts + 1):
	print "Starting with part %s..." % part

	# Open all files
	parsed_file = open(parse_fn % (kind, part), 'r')
	tag_features_file = open(tag_features_fn, 'w');
	bigram_features_file = open(bigram_features_fn, 'w');
	art_features_file = open(art_features_fn, 'w');
	prep_features_file = open(prep_features_fn, 'w');

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
		
		# Now loop through the candidate block and store the features
		# Note that this is very similar to when you generate the vocabularies
		for word_id, word_form, _, lemma, _, \
			tag, _, morph, _, head, _, _, _, _ in lines:
			head_info = lines[int(head) - 1]

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

			# Ratio singular / plural nouns
			# ratio male/female/neuter

		# Remove duplicates and sort (cause, hey, why not?)
		bigram_ids = set(sorted(bigram_ids))
		tag_ids = set(sorted(tag_ids))
		art_ids = set(sorted(art_ids))
		prep_ids = set(sorted(prep_ids))
		
		# Write results
		tag_features_file.write(ids2str(tag_ids) + "\n")
		bigram_features_file.write(ids2str(bigram_ids) + "\n")
		art_features_file.write(ids2str(art_ids) + "\n")
		prep_features_file.write(ids2str(prep_ids) + "\n")
		
		# reset
		lines = []

	# Close open files
	parsed_file.close()
	tag_features_file.close()
	bigram_features_file.close()
	art_features_file.close()
	prep_features_file.close()


