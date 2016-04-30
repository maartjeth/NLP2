import os

class Helper:
	"""
	The main helper class.
	It contains several usefull functions, but also several parameters
	that we use in all tasks.
	"""

	def __init__(self):
		self.num_sentences = 100

		self.sentences_fn 			= "../data/dev/dev-ooved.en"
		self.grammar_base_fn 		= "../data/rules.monotone.dev/grammar"
		self.sentences_fn 			= "../data/dev-ooved.en"
		self.input_fst_base 		= "../data/inputs/input"
		self.phrase_table_fst_base 	= "../data/phrase-tables/phrase-table"


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
			grammar.append('[X] ||| OOV ||| OOV ||| EgivenFCoherent=0 SampleCountF=0 CountEF=0 MaxLexFgivenE=0 MaxLexEgivenF=0 IsSingletonF=0')
		return [rule for rule in grammar if rule != ""]
    