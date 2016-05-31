import cPickle as pickle
from sklearn import svm
from sklearn.externals import joblib
import numpy as np

sample_size = 100
name = "defdata"

instances_fn = '../data-dev/classification/%s-instances-%s.pickle' % (name, sample_size)
labels_fn = '../data-dev/classification/%s-labels-%s.pickle' % (name, sample_size)
classifier_output_fn = "../data-dev/models/%s-classifier-%s.skl-pickle" % (name, sample_size)

with open(instances_fn, 'rb') as instances_file:
	instances = pickle.load(instances_file)
with open(labels_fn, 'rb') as labels_file:
	labels = pickle.load(labels_file)

N = -1
instances = instances[:N,:]
labels = labels.toarray().flatten()[:N]

clf = svm.LinearSVC()
clf.fit(instances, labels)

# Store the model
joblib.dump(clf, classifier_output_fn)