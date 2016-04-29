import os

class FST:

	def __init__(self, txtfst_base=""):
		"""Initialize

		Args:
			fst_file: the filename of the .txtfst fst-file. The label .isyms and .osyms
			files are assumed to be in the same directory.
		"""
		txtfst_fn = txtfst_base + ".txtfst"
		self.base, _ = os.path.splitext(txtfst_fn)
		self.dir = os.path.dirname(txtfst_fn)
		self.txtfst_fn = txtfst_fn
		self.isymbols_fn = self.base + '.isyms'
		self.osymbols_fn = self.base + '.osyms'
		self.fst_fn = self.base + '.fst'

	def update_osymbols(self, osymbols):
		"""
		Overwrites the .osyms file.
		"""
		with open(self.osymbols_fn, 'w') as f:
			f.write(osymbols)
		return self

	def update_isymbols(self, isymbols):
		"""
		Overwrites the .isyms file.
		"""
		with open(self.isymbols_fn, 'w') as f:
			f.write(isymbols)
		return self

	def update_fst(self, fst):
		"""
		Overwrites the (uncompiled) text file describing the fst 
		"""
		with open(self.txtfst_fn, 'w') as f:
			f.write(fst)
		return self

	def compile(self):
		"""Compile FST"""
		if os.path.isfile(self.isymbols_fn):
			call = "fstcompile --isymbols=%s --osymbols=%s %s %s" % (self.isymbols_fn, self.osymbols_fn, self.txtfst_fn, self.fst_fn)
		else:
			call = "fstcompile --osymbols=%s %s %s" % (self.osymbols_fn, self.txt_fn, self.fst_fn)
		subprocess.call([call], shell=True)
		return self

	def sort(self, override=True, how="ilabel"):
		"""
		Sorts the FST and saves the file in a .sorted.fst file

		Args:
			override: override the `.fst` file?
			how: either `ilabel` (default) or `olabel`
		"""
		self.sorted_fst_fn = self.fst_fn if override else self.base + '.sorted.fst'
		call = "fstarcsort --sort_type=%s %s %s" % (how, self.fst_fn, self.sorted_fst_fn)
		subprocess.call([call], shell=True)
		return self

	def draw(self, format="pdf"):
		"""
		Draws the FST in a format of choice (PDF, by default)

		Args:
			format: A format of choice (e.g. pdf, jpg, ps, png, etc.).
			see http://www.graphviz.org/doc/info/output.html for all formats
		"""
		# Check if the fst isn't too large
		with open(self.txtfst_fn, 'r') as f:
			num_lines = sum(1 for _ in f)
		if num_lines > 100: print "WARNING: drawing a very large FST (%s lines) can take a long time." % num_lines

		dot_fn = self.base + '.dot.tmp'
		calls = [
			"fstdraw --isymbols=%s --osymbols=%s %s %s" % (self.isymbols_fn, self.osymbols_fn, self.fst_fn, dot_fn),
			"dot -T%s %s -o %s.%s" % (format, dot_fn, self.base, format),
			"rm " + dot_fn
		]
		for call in calls:
			subprocess.call([call], shell=True)
		return self



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
		with open(grammar_base_fn + "." + str(i), 'r') as f:
			grammar = f.read().split("\n") # set dummy features to 0
			grammar.append('[X] ||| OOV ||| OOV ||| EgivenFCoherent=0 SampleCountF=0 CountEF=0 MaxLexFgivenE=0 MaxLexEgivenF=0 IsSingletonF=0')
		return [rule for rule in grammar if rule != ""]
    