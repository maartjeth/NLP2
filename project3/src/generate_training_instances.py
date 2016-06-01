"""
Generates training instances

This file generates training instances for all candidates listed in
a file with samples. All features are supposed to be in different files,
with every line corresponding to a candidate.

The resulting feature vectors are written to two files: one for positive
instance and one for negative instances.
"""
from Features import *

# Sample size in the PRO
sample_size = "10"

name = "defdata"

##############################################################

# Again, we don't need instances for the test set
kind = "dev"

# Output file for positive and negative classification instances
pos_instances_fn = "../data-%s/classification/%s-pos-instances-%s.txt" % (kind,name,sample_size)
neg_instances_fn = "../data-%s/classification/%s-neg-instances-%s.txt" % (kind,name,sample_size)

# Samples	
samples_fn = '../data-%s/samples/%s-samples-%s.txt' % (kind, kind, sample_size)

# File with 1000best training instances
candidates_fn = "../data/nlp2-%s.1000best" % kind

# File with all meteor scores
scores_fn = "../data-%s/eval/%s-meteor.txt" % (kind, kind)

# Sentences information
sentences_fn = '../data-%s/%s-sentences.json' % (kind, kind)
sentences = json.load(open(sentences_fn,'r'))

# Other feature files
# linguistic_features_fn = "../data-dev/ling-features/dev-ling-features.txt"
# ...

######### FEATURE OBJECTS ################################
# Feature objects. Add as many as you like...
#
def_features = DefFeatures(candidates_fn, samples_fn, sentences)
# ling_features = LinguisticCandidateFeatures(linguistic_features_fn, samples_fn, sentences)
# ...
all_features = [def_features] #, ling_feauters, ...
#####

# A object with all METEOR scores
scores = Scores(scores_fn, samples_fn, sentences)

def flatten(list_):
	return [item for sublist in list_ for item in sublist]

# Iterate over all samples and write out the training instances
pos_instances_file = open(pos_instances_fn, 'w')
neg_instances_file = open(neg_instances_fn, 'w')
for i, features in enumerate(izip(scores, *all_features)):	
	if i % 5000 == 0: print "%s Candidates done" % str(i).zfill(7)

	# Unpack the features
	cand1 = flatten([feat[0] for feat in features])
	cand2 = flatten([feat[1] for feat in features])
	score1 = cand1[0]
	score2 = cand2[0]
	cand1 = np.array(cand1[1:])
	cand2 = np.array(cand2[1:])
	
	# Find positive and negative instance
	if score1 > score2:
		winner, loser = cand1, cand2
	else:
		winner, loser = cand2, cand1
	pos_instance = winner - loser
	neg_instance = loser - winner

	# Save as comma-separated value
	pos_instances_file.write( ",".join(map(str, pos_instance)) + "\n" )
	neg_instances_file.write( ",".join(map(str, neg_instance)) + "\n" )

print('Done.')

# Wrap up
pos_instances_file.close()
neg_instances_file.close()
	