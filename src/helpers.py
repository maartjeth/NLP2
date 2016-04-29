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

def load_sentences(filename="../data/dev-ooved.en"):
	"""Returns the list of English sentences"""
	with open(filename, 'r') as f:
		sentences = f.read().split("\n")
	return [s for s in sentences if s != ""]




if __name__ == "main":
	print load_sentences()