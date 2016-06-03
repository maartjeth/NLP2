import cPickle as pickle
from sklearn import svm
from sklearn.externals import joblib
import numpy as np

sample_size = 100
name = "def-features"
kind = "dev"

instances_fn = '../data-%s/classification/%s-instances-%s.pickle' % (kind, name, sample_size)
labels_fn = '../data-%s/classification/%s-labels-%s.pickle' % (kind, name, sample_size)
classifier_output_fn = "../data-%s/models/%s-classifier-%s.skl-pickle" % (kind, name, sample_size)

with open(instances_fn, 'rb') as instances_file:
	instances = pickle.load(instances_file)
with open(labels_fn, 'rb') as labels_file:
	labels = pickle.load(labels_file)

print "Loading training instances..."
N = -1
instances = instances[:N,:]
labels = labels.toarray().flatten()[:N]

print "Fitting model..."
clf = svm.LinearSVC()
clf.fit(instances, labels)
print clf.coef_

# Store the model
print "Storing model..."
joblib.dump(clf, classifier_output_fn)