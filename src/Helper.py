import os
import subprocess

class Helper:
	"""
	The main helper class.
	It contains several usefull functions, but also several parameters
	that we use in all tasks.
	"""

	def __init__(self, type, root=None):

		self.OOV = "OOV"
		directories = []
		self.type = type
		self.sentences_start = 0

		if type == "all-monotone":
			if root == None: root = "../results/"
			self.num_sentences 				= 100
			self.raw_sentences_fn 			= "../data/dev.en"
			self.sentences_fn 				= root + "dev-ooved-mono.en"
			self.input_fst_base 			= root + "mono-inputs/mono-input"
			self.phrase_table_fst_base 		= root + "mono-phrase-tables/mono-phrase-table"
			self.translation_fst_base 		= root + "mono-translations/mono-translation"
			self.best_derivation_fst_base 	= root + "mono-derivations/mono-derivation"
			self.best_derivations_base 		= root + "mono-best-derivations/monotone"
			self.grammar_base_fn 			= "../data/rules.monotone.dev/grammar"
			self.weight_file 				= "../data/weights.monotone"
			self.translation_base 			= root + "monotone-translations"
			self.blue_scores_fn 			= root + "mono-bleu-scores.txt"
			directories						= [root, "mono-inputs", "mono-phrase-tables", 
												"mono-translations", "mono-derivations", 
												"mono-best-derivations","blue-scores"]
			directories = [root + d for d in directories]

		elif type == "all-lattice":
			if root == None: root = "../results/"
			self.num_sentences 				= 100
			self.raw_sentences_fn 			= "../data/dev.en"
			self.sentences_fn 				= root + "dev-ooved-lattice.en"
			self.input_fst_base 			= root + "lat-inputs/lat-input"
			self.phrase_table_fst_base 		= root + "lat-phrase-tables/lat-phrase-table"
			self.translation_fst_base   	= root + "lat-translations/lat-translation"	
			self.best_derivation_fst_base 	= root + "lat-derivations/lat-derivation"
			self.best_derivations_base 		= root + "lat-best-derivations/lattice"
			self.grammar_base_fn 			= "../data/rules.n-best.dev/grammar"	
			self.weight_file				= "../data/weights.lattice"
			self.translation_base 			= root + "lat-translations"
			self.permutations_fn 			= "../data/dev.enpp.nbest"
			self.blue_scores_fn 			= root + "lat-bleu-scores.txt"
			directories						= [root, "lat-inputs", "lat-phrase-tables", 
												"lat-translations", "lat-derivations", 
												"lat-best-derivations", "blue-scores"]
			directories = [root + d for d in directories]

		elif type == "blackdog-monotone":
			if root == None: root = "../dummydata/blackdog-monotone/"
			self.num_sentences				= 1
			self.raw_sentences_fn 			= "../dummydata/blackdog.raw.en"
			self.sentences_fn 				= root + "blackdog.en"
			self.input_fst_base 			= root + "input"
			self.phrase_table_fst_base 		= root + "phrase-table"
			self.translation_fst_base   	= root + "translation"	
			self.best_derivation_fst_base 	= root + "derivation"
			self.best_derivations_base 		= root + "best-derivations"
			self.grammar_base_fn 			= "../dummydata/blackdog"	
			self.weight_file				= "../data/weights.monotone"
			self.translation_base 			= "../dummydata/blackdog-monotone-translations"
			self.permutations_fn 			= "../dummydata/blackdog.perm"
			directories 					= [root]

		elif type == "blackdog-lattice":
			if root == None: root = "../dummydata/blackdog-lattice/"
			self.num_sentences				= 1
			self.raw_sentences_fn 			= "../dummydata/blackdog.raw.en"
			self.sentences_fn 				= root + "blackdog.en"
			self.input_fst_base 			= root + "input"
			self.phrase_table_fst_base 		= root + "phrase-table"
			self.translation_fst_base   	= root + "translation"	
			self.best_derivation_fst_base 	= root + "derivation"
			self.best_derivations_base 		= root + "best-derivations"
			self.grammar_base_fn 			= "../dummydata/blackdog"	
			self.weight_file				= "../data/weights.lattice"
			self.translation_base 			= "../dummydata/blackdog-lattice-translations"
			self.permutations_fn 			= "../dummydata/blackdog.perm"
			directories 					= [root] 

		elif type == "freundin-monotone":
			if root == None: root = "../dummydata/freundin-monotone/"
			self.num_sentences				= 1
			self.raw_sentences_fn 			= "../dummydata/freundin.raw.en"
			self.sentences_fn 				= root + "freundin.en"
			self.input_fst_base 			= root + "input"
			self.phrase_table_fst_base 		= root + "phrase-table"
			self.translation_fst_base   	= root + "translation"	
			self.best_derivation_fst_base 	= root + "derivation"
			self.best_derivations_base 		= root + "blackdog-monotone"
			self.grammar_base_fn 			= "../dummydata/freundin"	
			self.weight_file				= "../data/weights.monotone"
			self.translation_base 			= "../dummydata/freundin-monotone-translations"
			directories 					= [root]

		elif type == "freundin-lattice":
			if root == None: root = "../dummydata/freundin-lattice/"
			self.num_sentences				= 1
			self.raw_sentences_fn 			= "../dummydata/freundin.raw.en"
			self.sentences_fn 				= root + "freundin.en"
			self.input_fst_base 			= root + "input"
			self.phrase_table_fst_base 		= root + "phrase-table"
			self.translation_fst_base   	= root + "translation"	
			self.best_derivation_fst_base 	= root + "derivation"
			self.best_derivations_base 		= root + "blackdog-monotone"
			self.grammar_base_fn 			= "../dummydata/freundin"	
			self.weight_file				= "../data/weights.monotone"
			self.translation_base 			= "../dummydata/freundin-lattice-translations"
			self.permutations_fn 			= "../dummydata/freundin.perm"
			directories 					= [root]

		# Create missing directories		
		self.directories = directories
		if not os.path.isdir(root):
			os.makedirs(root)
		self.update_dirs(self.directories)

		self.features = ["IsSingletonF", "IsSingletonFE", "SampleCountF", "CountEF",
						 "EgivenFCoherent", "MaxLexEgivenF", "Glue", "WordPenalty",
						 "PassThrough", "LatticeCost"]#, "MaxLexFgivenE"]

	def update_dirs(self, directories=None):
		if directories==None: directories = self.directories
		for directory in self.directories:
			if not os.path.isdir(directory):
				os.makedirs(directory)

	def get_sentences(self, sentences_fn=None):
		"""
		Returns the list of English sentences
		"""
		if sentences_fn == None: sentences_fn = self.sentences_fn
		with open(sentences_fn, 'r') as f:
			sentences = f.read().split("\n")
		return [s for s in sentences if s != ""]

	def get_grammar(self, i, grammar_base_fn=None):
		"""
		Retrieve a grammar (list of rules) by its sentence number
		"""
		if grammar_base_fn == None: grammar_base_fn = self.grammar_base_fn
		with open(grammar_base_fn + "." + str(i), 'r') as f:
			grammar = f.read().split("\n") # set dummy features to 0
			grammar.append('[X] ||| %s ||| %s ||| EgivenFCoherent=0 SampleCountF=0 CountEF=0 MaxLexFgivenE=0 MaxLexEgivenF=0 IsSingletonF=0' % (self.OOV, self.OOV))
		return [rule for rule in grammar if rule != ""]

	def dump_bleu_scores(self):
		"""
		Writes the bleu scores to a file.
		"""
		out = "BLEU SCORES for '%s'\n\n" % self.type
		for method in ["viterbi", "map"]:
			out += "\tMethod: %s \n" % method

			call = "../data/./multi-bleu.perl ../data/dev.ja < %s.%s > __tmp.txt" % (self.translation_base, method)
			subprocess.call([call], shell=True)

			with open("__tmp.txt", "r") as f:
				out += "\t%s\n" % f.read()
			os.remove("__tmp.txt")
		
		out += "\nFEATURE WEIGHTS\n"
		for feature, val in self.get_feature_weights().iteritems():
			out += "\n\t%s: %s" % (feature, val)

		out += "\n\nNUM SENTENCES: %s" % self.num_sentences

		with open(self.blue_scores_fn, "w") as f:
			f.write(out)

		return out


    