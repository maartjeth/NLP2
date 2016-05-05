import subprocess
import os
import warnings

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

		# The quantization delta of OpenFST
		self.delta = 10**(-15);

	def is_empty(self):
		if os.path.isfile(self.txtfst_fn):
			return os.stat(self.txtfst_fn).st_size == 0
		else:
			print "decompiling..."
			self.decompile()
			return self.is_empty()

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
		isyms = " --isymbols="+self.isymbols_fn if os.path.isfile(self.isymbols_fn) else "";
		osyms = " --osymbols="+self.osymbols_fn if os.path.isfile(self.osymbols_fn) else "";
		call = "fstcompile%s%s %s %s" % (isyms, osyms, self.txtfst_fn, self.fst_fn)
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
	
	def sort2(self,  how="ilabel", new_fst_base=False, in_place=False):
		"""
		Sorts the FST and saves the file in a .sorted.fst file

		Args:
			override: override the `.fst` file?
			how: either `ilabel` (default) or `olabel`
		"""
		print "sorting", new_fst_base
		if new_fst_base == False: return self.sort(new_fst_base=self.base, in_place=True)

		call = "fstarcsort --sort_type=%s %s %s" % (how, self.fst_fn, new_fst_base)
		subprocess.call([call], shell=True)


		if in_place: 
			self.decompile()
			return self
		new_fst = FST(new_fst_base)
		new_fst.isymbols_fn = self.isymbols_fn
		new_fst.osymbols_fn = self.osymbols_fn
		return new_fst

	def draw(self, format="pdf"):
		"""
		Draws the FST in a format of choice (PDF, by default)

		Args:
			format: A format of choice (e.g. pdf, jpg, ps, png, etc.).
			see http://www.graphviz.org/doc/info/output.html for all formats
		"""
		# Check if the fst isn't too large and otherwise throw a warning
		if os.path.isfile(self.txtfst_fn):
			with open(self.txtfst_fn, 'r') as f:
				num_lines = sum(1 for _ in f)
			if num_lines > 100: 
				warnings.warn("Very large FST: drawing a very large FST (%s lines) can take a long time." % num_lines)

		dot_fn = self.base + '.dot.tmp'
		drawing = self.base + "." + format 

		# If the FST is empty, throw a warning
		if self.is_empty():
			if os.path.isfile(drawing):
				os.rename(drawing, "%s.old.%s" % (self.base, format))
			warnings.warn("Cannot draw an empty fst. Returning...")
			return False

		# Ok, good to go, draw!
		isyms = " --isymbols="+self.isymbols_fn if os.path.isfile(self.isymbols_fn) else "";
		osyms = " --osymbols="+self.osymbols_fn if os.path.isfile(self.osymbols_fn) else "";
		calls = [
			"rm -f " + drawing,
			"fstdraw%s%s --portrait=true %s %s" % (isyms, osyms, self.fst_fn, dot_fn),
			"dot -T%s %s -o %s" % (format, dot_fn, drawing),
			"rm " + dot_fn
		]
		for call in calls:
			subprocess.call([call], shell=True)
		return self

	def compose(self, other_fst, new_fst_base):
		"""
		Composes the current FST with another one. The other FST will
		first be sorted by its ilabels.
		"""
		other_fst.sort(how="ilabel")
		call = "fstcompose %s %s %s.fst" %  (self.fst_fn, other_fst.fst_fn, new_fst_base)
		subprocess.call([call], shell=True)

		# Postprocess new FST
		new_fst = FST(new_fst_base)
		new_fst.isymbols_fn = self.isymbols_fn
		new_fst.osymbols_fn = other_fst.osymbols_fn
		new_fst.decompile()
		if new_fst.is_empty():
			warnings.warn("Empty FST: Composing %s and %s INTO %s yields an empty FST" % (self.fst_fn, other_fst.fst_fn,new_fst.fst_fn))

		return new_fst

	def decompile(self, txtfst_fn=None):
		""" 
		Decompiles an FST into a "readable" text file
		"""
		self.txtfst_fn = self.txtfst_fn if txtfst_fn == None else txtfst_fn 
		isyms = " --isymbols="+self.isymbols_fn if os.path.isfile(self.isymbols_fn) else "";
		osyms = " --osymbols="+self.osymbols_fn if os.path.isfile(self.osymbols_fn) else "";
		call = "fstprint%s%s %s %s" % (isyms, osyms, self.fst_fn, self.txtfst_fn)
		subprocess.call([call], shell=True)
		return self

	def find_n_best(self, n, short_fst_base):
		""" 
		Finds the n-best paths in an fst
		""" 

		call = "fstshortestpath --nshortest=%s --delta=%s %s %s.fst" \
				% (n, self.delta, self.fst_fn, short_fst_base)
		subprocess.call([call], shell=True)

		# TODO: are these really the correct isymbols and osymbols??
		# Bas: seems like it!
		n_best_fst = FST(short_fst_base)
		n_best_fst.isymbols_fn = self.isymbols_fn
		n_best_fst.osymbols_fn = self.osymbols_fn

		return n_best_fst

	def copy_symbols(self):
		isyms_fn = self.base + ".isyms"
		osyms_fn = self.base + ".osyms" 
		call = "cp %s %s; cp %s %s;" % (self.isymbols_fn, isyms_fn, self.osymbols_fn, osyms_fn)
		subprocess.call([call], shell=True)

	def determinize(self, new_fst_base=False, in_place=False):
		"""
		Determinizes the current FST.
		If new_fst_base is False, the current FST is updated
		"""
		if new_fst_base == False: return self.determinize(self.base, True)

		call = "fstdeterminize --delta=%s %s %s.fst" \
				% (self.delta, self.fst_fn, new_fst_base)
		subprocess.call([call], shell=True)

		if in_place: return self
		new_fst = FST(new_fst_base)
		new_fst.isymbols_fn = self.isymbols_fn
		new_fst.osymbols_fn = self.osymbols_fn
		return new_fst

	def push(self, new_fst_base=False, in_place=False):
		"""
		If new_fst_base is False, the current FST is updated
		"""
		if new_fst_base == False: return self.push(self.base, True)

		call = "fstpush --push_weights=true --delta=%s %s %s.fst" \
				% (self.delta, self.fst_fn, new_fst_base)
		subprocess.call([call], shell=True)

		if in_place: return self
		new_fst = FST(new_fst_base)
		new_fst.isymbols_fn = self.isymbols_fn
		new_fst.osymbols_fn = self.osymbols_fn
		return new_fst

	def minimize(self, new_fst_base=False, in_place=False):
		"""
		Minimize an FST
		If new_fst_base is False, the current FST is updated
		"""
		if new_fst_base == False: return self.minimize(self.base, True)

		call = "fstminimize --delta=%s %s %s.fst" \
				% (self.delta, self.fst_fn, new_fst_base)
		subprocess.call([call], shell=True)
		
		if in_place: return self
		new_fst = FST(new_fst_base)
		new_fst.isymbols_fn = self.isymbols_fn
		new_fst.osymbols_fn = self.osymbols_fn
		return new_fst


