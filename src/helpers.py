import subprocess
import os

class FST:
	def __init__(self, fst_file = ""):
		"""Initialize

		Args:
			fst_file: the filename of the .fst file. The other files (.isyms, .osyms)
			are assumed to be in the same directory
		"""
		self.base, _ = os.path.splitext(fst_file)
		self.dir = os.path.dirname(fst_file)
		self.fst_fn = fst_file
		self.isymbols_fn = self.base + '.isyms'
		self.osymbols_fn = self.base + '.osyms'
		self.binary_fn = self.base + '.bin'

	
	def update_osymbols(self, osymbols):
		with open(self.osymbols_fn, 'w') as f:
			f.write(osymbols)

	def update_isymbols(self, isymbols):
		with open(self.isymbols_fn, 'w') as f:
			f.write(isymbols)

	def update_fst(self, fst):
		with open(self.fst_fn, 'w') as f:
			f.write(fst)

	def compile(self):
		"""Compile FST"""
		if os.path.isfile(self.isymbols_fn):
			call = "fstcompile --isymbols=%s --osymbols=%s %s %s" % (self.isymbols_fn, self.osymbols_fn, self.fst_fn, self.binary_fn)
		else:
			call = "fstcompile --osymbols=%s %s %s" % (self.osymbols_fn, self.fst_fn, self.binary_fn)
		# 	print os.getcwd()
		# print call
		subprocess.call([call], shell=True)


#######
# Other helpers

class Helper:
	"""
	The main helper class.
	It contains several usefull functions, but also several parameters
	that we use in all tasks.
	"""

	def __init__(self):
		self.num_sentences = 100
		self.sentences_fn = "../data/dev/dev-ooved.en"
		self.grammar_base_fn = "../data/rules.monotone.dev/grammar"
		self.sentences_fn = "../data/dev-ooved.en"


	def load_sentences(self, sentences_fn=None):
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
		with open(grammar_base_fn + "." + str(i)) as f:
			grammar = f.read().split("\n") # set dummy features to 0
			grammar.append('[X] ||| OOV ||| OOV ||| EgivenFCoherent=0 SampleCountF=0 CountEF=0 MaxLexFgivenE=0 MaxLexEgivenF=0 IsSingletonF=0 oov=1')
		return grammar
    



if __name__ == "main":
	print load_sentences()