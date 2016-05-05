import os

class Helper:
	"""
	The main helper class.
	It contains several usefull functions, but also several parameters
	that we use in all tasks.
	"""

	def __init__(self, type="monotone"):

		self.num_sentences 					= 100
		self.raw_sentences_fn 				= "../data/dev.en"
		# self.best_derivation_fst_base 	= "../data/4-best-mono-derivations/mono-translation"
		# self.best_derivations_base 		= "../data/4-best-mono-derivations/monotone"
		self.OOV = "OOV"

		# difference between task 5 and the rest:
		if type == "lattice":
			self.sentences_fn 				= "../data/dev-ooved-lattice.en"
			self.input_fst_base 			= "../data/5-input-lattices/input-lattice"
			self.phrase_table_fst_base 		= "../data/5-phrase-tables/phrase-table"
			self.translation_fst_base   	= "../data/6-lattice-translations/lattice-translation"	
			self.best_derivation_fst_base 	= "../data/6-best-lattice-derivations/lattice-derivation"
			self.best_derivations_base 		= "../data/6-best-lattice-derivations/lattice"
			self.grammar_base_fn 			= "../data/rules.n-best.dev/grammar"	
			self.weight_file				= "../data/weights.lattice"
			self.translation_base 			= "../data/lattice-translations"

		else:
			self.sentences_fn 				= "../data/dev-ooved-mono.en"
			self.input_fst_base 			= "../data/1-inputs/input"
			self.phrase_table_fst_base 		= "../data/2-phrase-tables/phrase-table"
			self.translation_fst_base 		= "../data/3-mono-translations/mono-translation"
			# FIX NAME:
			self.best_derivation_fst_base 	= "../data/4-best-mono-derivations/mono-translation"
			self.best_derivations_base 		= "../data/4-best-mono-derivations/monotone"
			self.grammar_base_fn 			= "../data/rules.monotone.dev/grammar"
			self.weight_file 				= "../data/weights.monotone"
			self.translation_base 			= "../data/monotone-translations"


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
    