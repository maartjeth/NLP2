import os
from Features import *
import random
from scipy.sparse import coo_matrix
from scipy.sparse import csr_matrix
from sklearn import svm
from sklearn.externals import joblib
import cPickle as pickle
import numpy as np
from time import time
import cProfile

class Model:

	# File with all candidates
	candidates_fn = "{root}/data/nlp2-{kind}.1000best"

	# File with all METEOR scores of all candidates
	pro_scores_fn = "{root}/data-{kind}/{kind}-meteor.txt"

	# JSON file with information about all sentences
	sentences_fn = "{root}/data-{kind}/{kind}-sentences.json"

	# File with a sample of candidates per sentence
	samples_fn = "{root}/data-{kind}/samples/{kind}-samples-{sample_size}.txt"

	# File with feature values for every candidate
	features_fn = "{root}/data-{kind}/features/{kind}-{feature}-features.txt"

	# File with feature vocabulary
	features_voc_fn = "{root}/data-{kind}/features/{kind}-{feature}-vocabulary.pickle"

	# Root directory of the model
	model_dir = "{root}/models/{name}" 

	# Training instances
	training_instances_fn = "{root}/models/{name}/{name}-training-instances.pickle"
	training_labels_fn = "{root}/models/{name}/{name}-training-labels.pickle"
	
	# The scikit-learn model
	model_fn = "{root}/models/{name}/{name}.model"

	# A file with the candidate ranking of the test sentences
	ranking_fn = "{root}/models/{name}/{name}-ranking-{test_name}.txt"
	best_translations_fn = "{root}/models/{name}/{name}-best-translations-{test_name}.txt"

	log_fn = "{root}/models/{name}/{name}-log-{i}.txt"

	# All possible slugs
	slugs = ['candidates', 'pro_scores', 'sentences', 'features', 
			 'training_instances', 'training_labels', 'model']

	# Slugs of the features
	feature_slugs = ['def', 'tag', 'bigram']

	# Features with vocabularies
	feature_vocs = ['bigram', 'tag']

	# Dictionary with options
	opts = {
		'root': ".."
	}

	# Dictionary with all files (open/closed)
	files = {}

	# A log
	__log = ""

	# The actual model (classifier) and its feature weights
	model = None
	weights = None
	
	def __init__(self, name, kind, sample_size, features, **kwargs):
		self.time = time()
		self.time0 = time()
		# Store all options
		self.opts.update({
			'kind': kind,
			'sample_size': sample_size,
			'name': name,
			'features':features
		})
		self.name = name
		self.kind = kind
		self.sample_size = sample_size
		self.used_features = features

		# Override filenames
		if 'samples_fn' in kwargs:
			self.samples_fn = kwargs['samples_fn']

		if 'pro_scores_fn' in kwargs:
			self.pro_scores_fn = kwargs['pro_scores_fn']

		# Load sentences
		with self.open('sentences','r', kind="dev") as file:
			self.dev_sentences = json.load(file)
		with self.open('sentences','r', kind="test") as file:
			self.test_sentences = json.load(file)

		# Make folders
		model_dir = self.model_dir.format(**self.opts)
		if not os.path.exists(model_dir):
			os.makedirs(model_dir)

		# Log stuff
		self.log("{l}" + "{:*^80}\n".format(name.upper()) + "{l}", False)
		self.log_options()
		self.log_files()
		self.log("\n{l}", False)

	def fn(self, slug, **kwargs):
		"""
		Returns a filename by a name: so `candidate_scores` might return
		../data-dev/dev-meteor.txt.
		"""
		formatting = { 
			"root": self.opts['root'],
			"kind": self.kind,
			"sample_size": self.sample_size,
			"name": self.name
		}
		formatting.update(kwargs)
		return getattr(self, slug+"_fn").format(**formatting)

	def open(self, slug, how="r", **kwargs):
		"""Open a file by its slug."""
		fn = self.fn(slug, **kwargs)
		file = open(fn, how)
		self.files[fn] = file
		return file

	def close(self, slug, **kwargs):
		"""Close a file by its slug"""
		try:
			self.files[self.fn(slug, **kwargs)].close()
		except AttributeError: pass

	def log(self, text, live=True):
		text = text.format(l="*"*80+"\n")
		if live: 
			print text
			diff0 = time() - self.time0
			diff  = time() - self.time
			self.time = time()
			self.__log += "{text:80} [d={diff:9.5f};t={time:9.5f}]\n".format(text=text, time=diff0, diff=diff)
		else:
			self.__log += "{text}\n".format(text=text)

	def log_files(self):
		self.log("Files", False)
		for slug in [s for s in self.slugs if s != "features"]:
			fn = self.fn(slug)
			if os.path.isfile(self.fn(slug)) == False:
				self.log("  * The {slug} file does not exist: {fn}".format(slug=slug, fn=fn), False)
			else:
				self.log("  . {slug} file: {fn}".format(slug=slug, fn=fn), False)
		
		# Check feature files
		for feat in self.feature_slugs:
			fn = self.fn('features', feature=feat)
			if os.path.isfile(fn) == False:
				self.log("  * {feat} features file does not exist: {fn}".format(feat=feat, fn=fn), False)
			else:
				self.log("  . {feat} features: {fn}".format(feat=feat, fn=fn), False)

		for feat in self.feature_vocs:
			fn = self.fn('features_voc', feature=feat)
			if os.path.isfile(fn) == False:
				self.log("  * {feat} feature vocabulary file does not exist: {fn}".format(feat=feat, fn=fn), False)
			else:
				self.log("  . {feat} feature voc: {fn}".format(feat=feat, fn=fn), False)

	def log_options(self):
		self.log("Options", False)
		for key, val in self.opts.items():
			self.log("  * {key}: {value}".format(key=key, value=val), False)
		self.log("", False)

	def write_log(self):
		i = 0
		while os.path.exists(self.fn('log', i=i)) == True:
			i += 1

		log_file = self.open('log', i=i, how="w")
		log_file.write(self.__log)
		log_file.close()

	def get_sentences(self, kind=None):
		if kind == None: kind = self.kind
		return getattr(self, kind + "_sentences")

	def get_features(self, kind=None):
		"""Initializes a list with all feature objects"""
		if kind == None: kind = self.kind
		samples_fn = self.fn('samples')
		sentences = self.get_sentences(kind)
		features = []

		if 'def' in self.used_features:
			features_fn = self.fn('candidates', kind=kind)
			def_feat = DefFeatures(features_fn, samples_fn, sentences)
			features.append(def_feat)

		# Get sparse features
		for feature in 'tag bigram prep es artpl prepart'.split():
			if feature not in self.used_features: continue

			voc_size 	= get_voc_size(self.fn('features_voc', feature=feature))
			features_fn = self.fn('features', feature=feature, kind=kind)
			sparse_feat = SparseFeatures(voc_size, features_fn, samples_fn, sentences)
			features.append(sparse_feat)

		for feature in 'ratios art wordcount def-combined'.split():
			if feature not in self.used_features: continue

			features_fn = self.fn('features', feature=feature, kind=kind)
			dense_feat = DenseFeatures(features_fn, samples_fn, sentences)
			features.append(dense_feat)

		return features

	def generate_training_instances(self):
		self.log("Generating training instances")

		# Load features and scores for Pro algorithm
		feature_iterators = self.get_features()
		scores = Scores(self.fn('pro_scores'), self.fn('samples'), self.get_sentences())
		
		# Build random ordering
		with self.open('samples') as file:
			num_lines = 0
			for _ in file: num_lines += 1
		num_candidates =  num_lines * self.sample_size * 2
		ordering = range(num_candidates)
		random.shuffle(ordering)
		
		# COO matrix!
		rows, cols, vals = [], [], []
		labels = np.zeros(num_candidates)
		for i, features in enumerate(izip(scores, *feature_iterators)):	
			if i>6000: break
			if i % 5000 == 0: self.log("  {i:>6}/{num_candidates} candidates done".format(i=i, num_candidates=num_candidates))

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
			
			pos_index = ordering[2*i]
			neg_index = ordering[2*i+1]
			
			# Update labels (negative index is already 0)
			labels[pos_index] = 1
			
			# Store sparse data
			pos_non0 = pos_instance.nonzero()[0]
			neg_non0 = neg_instance.nonzero()[0]

			rows += [pos_index] * len(pos_non0) 	+ [neg_index] * len(neg_non0)
			cols += pos_non0.tolist() 				+ neg_non0.tolist()
			vals += pos_instance[pos_non0].tolist() + neg_instance[neg_non0].tolist()

		self.log("  Sparsifying training instances...")
		instances = coo_matrix((vals, (rows, cols)), shape=(len(ordering), len(pos_instance)))

		self.log("  Storing training instances...")
		instances_file = self.open('training_instances', 'wb')
		labels_file = self.open('training_labels', 'wb')
		pickle.dump(instances, instances_file, pickle.HIGHEST_PROTOCOL)
		pickle.dump(labels, labels_file, pickle.HIGHEST_PROTOCOL)
		instances_file.close()
		labels_file.close()

		# Returning
		self.log("  Done. Stored %s instances with %s features each." % instances.shape)
		return instances, labels
	
	def get_training_instances(self):
		"""Retrieves or generates training instances"""
		try: 
			instances_file = self.open('training_instances', 'rb')
			labels_file = self.open('training_labels', 'rb')
			instances = pickle.load(instances_file)
			labels = pickle.load(labels_file)
			return instances, labels
		except IOError:
			self.log("Training instances could not be found, generating new ones...")
			return self.generate_training_instances()

	def fit(self):
		"""Fits a Linear SVC model to the training instances"""
		instances, labels = self.get_training_instances()
		# labels = labels.toarray().flatten()
		self.log("Fitting model...")
		self.model = svm.LinearSVC()
		self.model.fit(instances, labels)
		self.weights = self.model.coef_

		self.log("Storing model...")
		joblib.dump(self.model, self.fn('model'))

		self.log("  Done.")

	def load(self):
		"""Loads the model"""
		try:
			self.log("Loading model...")
			self.model = joblib.load(self.fn('model'))
			self.weights = self.model.coef_
			self.log("  Done.")
		except IOError:
			self.log("The model could not be loaded...")
			raise IOError('The model could not be found. Perhaps you have to fit it firt?')

	def rerank(self, test_name, exclude=[], kind="test"):
		self.log("Reranking translations...")

		# Open output files
		ranking_file = self.open('ranking', test_name=test_name, how="w")
		best_translations_file = self.open('best_translations', test_name=test_name, how="w")

		sentence_features = []
		for features in self.get_features(kind=kind):
			sentence_features.append(features.iter_sentences())

		translation_expr = re.compile(" \|\d+-\d+\| ")
		exclude = sorted(exclude)[::-1]

		for i, sentence_features in enumerate(izip(*sentence_features)):
			if i % 100 == 0: self.log("  {:>4} candidates done".format(i))
			# if i>=3: break

			# Skip sentences that we have to exclude
			if len(exclude) > 0 and i == exclude[-1]:
				exclude.pop()
				continue	
			
			# Note that:
			# features_i, lines_i = sentence_features[i]
			candidate_lines = sentence_features[0][1]

			# combine lists of features
			features = []
			for i in range(len(candidate_lines)):
				flat = flatten([ feat[0][i] for feat in sentence_features ]) 
				features.append(flat)

			# Calculate the scores of the sentence
			scores = self.weights.dot(np.array(features).T)[0]
			
			# Get the ranking.
			# Note that argsort returns the lowest score first
			ranking = np.argsort(scores)[::-1]
			ranking_file.write(ids2str(ranking) + "\n")

			# Extract the best translation
			best = candidate_lines[ranking[0]]
			parts = best.split(" ||| ")
			words = translation_expr.split(parts[1])
			translation = " ".join(words)
			best_translations_file.write(translation + "\n")

		ranking_file.close()
		best_translations_file.close()
		self.log("  Done.")

def flatten(list_):
	return [item for sublist in list_ for item in sublist]			

def ids2str(lst):
	return ",".join(map(str, lst))

if __name__ == "__main__":
	M = Model("test-def-tag-bigram-50", kind="dev", sample_size=50, 
		# features=['ratios'])
		features=['def', 'tag', 'wordcount'])#'bigram', 'artpl', 'es', 'prep', 'prepart'])#, 'def-combined-2'])
	# print M.get_features()
	M.generate_training_instances()
	# cProfile.run('M.generate_training_instances()')
	# M.fit()
	# M.load()
	
	# # # exclude = [i for i in range(len(M.sentences)) if i not in val_sentences]
	# M.rerank("results")
	# M.write_log()

