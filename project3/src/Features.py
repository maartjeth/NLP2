from itertools import izip
import json
import numpy as np
import re
import pickle as pickle
from sklearn import svm

class Features:
	"""
	This class allows you retrieve all candidate features in 
	a memory-efficiant fashion. It reads all candidates of a
	sentence into memory, then selects the sample and yields
	`(features_cand_1, features_cand2)`.

	A subclass should implement the `get_features` method, 
	which extracts the features from a line in the file.
	"""

	def __init__(self, features_fn, samples_fn, sentences, n_poly=None):
		"""
		features_fn: a file with features of every candidate. 
		samples_fn: a file with all samples
		sentences: a list of dictionaries that at least contain
			a `first_line` and a `last_line` of every sentence
		"""
		self.features_fn = features_fn
		self.samples_fn = samples_fn
		self.sentences = sentences
		self.n_poly = n_poly
		
	def __iter__(self):
		self.sample_features = self.iter_samples()
		return self	

	def next(self):
		return self.sample_features.next()

	def get_features(self, line):
		raise NotImplementedError('The method get_features is not implemented!')

	def iter(self):
		"""Iterates over all features"""
		with open(self.features_fn, 'r') as features_file:
			for line in features_file:
				yield self.get_features(line)

	def iter_sentences(self):
		features_file = open(self.features_fn, 'r')
		line_nr = -1
		for sentence in self.sentences:
			features = []
			lines = []
			while True:
				line_nr += 1
				line = features_file.next()
				lines.append(line)
				features.append(self.get_features(line))
				if sentence['last_line'] == line_nr:
					yield sentence, features, lines
					break
				

	def iter_samples(self):
		"""Iterates over the features of the candidates in the samples file"""
		line_nr = 0
		samples_file = open(self.samples_fn, 'r')
		features_file = open(self.features_fn, 'r')
	
		for cur_sentence, sample in enumerate(samples_file):
			# Skip empty samples
			if sample == "\n": continue

			# Get sample
			sample = map(int, sample.replace("\n","").split(","))
			
			# Get features of all candidate translations for this sentence
			features = []
			while True:

				# Load the next features
				line_nr += 1
				line = features_file.next()
				features.append(self.get_features(line))

				# Last line of this sentence?
				if self.sentences[cur_sentence]['last_line'] == line_nr:
					first_line = self.sentences[cur_sentence]['first_line']
					sample_feat = [features[s - first_line] for s in sample]
					for feat1, feat2 in zip(sample_feat[::2], sample_feat[1::2]):
						yield (feat1, feat2)
					break

		samples_file.close()
		features_file.close()


class DefFeatures(Features):

	def get_features(self, line):
		line = line.replace("\n","")
		sentence, r_translation, r_features, \
			system_score, r_alignment, source = line.split(" ||| ")

		features = []
		parts = re.split("\s?([A-Za-z0-9]+)=\s?", r_features)[1:]
		for j in range(0, len(parts) - 1, 2):
			name = parts[j]
			if name in ['InputFeature0']: continue
			feat = map(float, parts[j+1].split())
			features += feat

class CombineFeatures(Features):

	def get_features(self, line):
		kind = 'dev'
		line = line.replace("\n","")
		sentence, r_translation, r_features, \
			system_score, r_alignment, source = line.split(" ||| ")

		features = []
		parts = re.split("\s?([A-Za-z0-9]+)=\s?", r_features)[1:]
		for j in range(0, len(parts) - 1, 2):
			name = parts[j]
			if name in ['InputFeature0']: continue
			feat = map(float, parts[j+1].split())
			features += feat

		if poly != None:
			poly = PolynomialFeatures(self.n_poly)
			features = poly.fit_transform(features)

		combined_features_fn = "../data-%s/combined-features%s.txt" % (kind, self.n_poly)
		with open(combined_features_fn, 'a') as comb_f_f:
			comb_f_f.write(features)
		
		return features

class Scores(Features):
	def get_features(self, line):
		return [float(line.replace("\n", ""))]

class SparseFeatures(Features):
	def __init__(self, voc_size, *args):
		Features.__init__(self, *args)
		self.voc_size = voc_size

	def get_features(self, line):
		features = np.zeros(self.voc_size, dtype=int)
		indices = map(int, line.replace("\n", "").split(","))
		features[indices] = 1
		return features

def get_voc_size(voc_fn):
	with open(voc_fn, 'rb') as file:
		voc = pickle.load(file)
		return len(voc)


	
# class LinguisticFeatures(Features):
# 	def get_features(self, line):
		# Code to process a line
		
# if __name__ == "__main__":

# 	kind, sample_size = "dev", 10

# 	# Samples	
# 	samples_fn = '../data-%s/samples/%s-samples-%s.txt' % (kind, kind, sample_size)

# 	# Sentences information
# 	sentences_fn = '../data-%s/%s-sentences.json' % (kind, kind)
# 	sentences = json.load(open(sentences_fn,'r'))
	
# 	# File with 1000best training instances
# 	features_voc_fn = "../data-%s/ling-features/bigram-vocabulary.pickle" % kind
# 	features_fn = "../data-%s/ling-features/bigram-features.txt" % kind
# 	feature_voc_size = get_voc_size(features_voc_fn)
# 	f = SparseFeatures(feature_voc_size, features_fn, samples_fn, sentences)

# 	for i, feat in enumerate(f):
# 		if i>10: break
# 		print list(feat[0])
# 		len(feat[0])
