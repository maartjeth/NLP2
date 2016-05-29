from itertools import izip
import json
import numpy as np
import re

class CandidateFeatures:
	"""
	This class allows you retrieve all candidate features in 
	a memory-efficiant fashion. It reads all candidates of a
	sentence into memory, then selects the sample and yields
	`(features_cand_1, features_cand2)`.

	A subclass should implement the `get_features` method, 
	which extracts the features from a line in the file.
	"""

	def __init__(self, features_fn, samples_fn, sentences):
		"""
		features_fn: a file with features of every candidate. 
		samples_fn: a file with all samples
		sentences: a list of dictionaries that at least contain
			a `first_line` and a `last_line` of every sentence
		"""
		self.features_fn = features_fn
		self.samples_fn = samples_fn
		self.sentences = sentences
		
	def __iter__(self):
		self.candidate_features = self.get_candidate_features()
		return self	

	def next(self):
		return self.candidate_features.next()

	def get_features(self, line):
		raise NotImplementedError('The method get_features is not implemented!')

	def get_candidate_features(self):
		line_nr = 0
		with open(self.samples_fn, 'r') as samples_file:
			with open(self.features_fn, 'r') as features_file:
				for cur_sentence, sample in enumerate(samples_file):

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

class DefCandidateFeatures(CandidateFeatures):
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

		return features

class CandidateScores(CandidateFeatures):
	def get_features(self, line):
		return [float(line.replace("\n", ""))]

# class LinguisticCandidateFeatures(CandidateFeatures):
# 	def get_features(self, line):
		# Code to process a line
	

