"""
Preprocess the positive and negative training instances.

Positive instances are labelled 1 and negative instances 0.
After shuffling the instances, both instances and labels,
represented as sparse csr_matrices are pickled.

This should not take very long: ~6s for sample size 100
"""

# Sample size
sample_size = 100

# Name of the model
name = "defdata"

# Input files
pos_instances_fn = "../data-dev/classification/%s-neg-instances-%s.txt" %  (name, sample_size)
neg_instances_fn = "../data-dev/classification/%s-neg-instances-%s.txt" %  (name, sample_size)

# Output files
instances_output_fn = '../data-dev/classification/%s-instances-%s.pickle' %  (name, sample_size)
labels_output_fn = '../data-dev/classification/%s-labels-%s.pickle' % (name, sample_size)

###################################################################

import numpy as np
from scipy.sparse import csr_matrix
import cPickle as pickle

def csv2array(csv):
	return map(float, csv.split(","))

def read_instances_file(fn, positive, limit=-1):
	with open(fn, 'r') as file:
		instances = file.read().split("\n")[:limit]
		instances = [inst for inst in instances if inst != ""]
		instances = np.array( map(csv2array, instances) )

		# Add labels as a first row
		if positive:
			labels = np.ones((instances.shape[0],1))
		else:
			labels = np.zeros((instances.shape[0],1))
		return np.concatenate((labels, instances), axis=1)


# Load all instances in one num_instances x num_features matrix
labelled_positives = read_instances_file(pos_instances_fn, True)
labelled_negatives = read_instances_file(neg_instances_fn, False)
labelled_instances = np.concatenate((labelled_positives, labelled_negatives), axis=0)
del labelled_positives, labelled_negatives

# Randomly shuffle all rows (instances)
np.random.shuffle(labelled_instances)

# Separate labels and instances and sparsify
labels = csr_matrix(labelled_instances[:,0])
instances = csr_matrix(labelled_instances[:,1:])
del labelled_instances

# Store!
with open(instances_output_fn, 'wb') as output_file:
	pickle.dump(instances, output_file, pickle.HIGHEST_PROTOCOL)

with open(labels_output_fn, 'wb') as output_file:
	pickle.dump(labels, output_file, pickle.HIGHEST_PROTOCOL)



