import subprocess
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
		if os.path.isfile(self.txtfst_fn):
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

	def compose(self, other_fst, new_fst_base):
		call = "fstcompose %s %s %s.fst" %  (self.fst_fn, other_fst.fst_fn, new_fst_base)
		subprocess.call([call], shell=True)

		new_fst = FST(new_fst_base)
		new_fst.isymbols_fn = self.isymbols_fn
		new_fst.osymbols_fn = other_fst.osymbols_fn
		return new_fst

