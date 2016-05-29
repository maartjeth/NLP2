"""
Pre-processes files for parsing. 
The to-be-parsed file is turned into this weird
format with loads of tabs and underscores.
"""
import os
import subprocess

def prepare_parse(source_fn, target_fn, compress=True):
	print("Preparsing %s to %s" % (source_fn, target_fn))
	if os.path.isfile(source_fn) == False: return False
	with open(target_fn, 'w') as fn:
		with open(source_fn) as all_sents:
			for i, line in enumerate(all_sents):
				CoNLL_lines = ""
				for num, token in enumerate(line.split()):
					CoNLL_lines += "%s\t%s\t%s\t_\t_\t_\t_\t_\t_\t_\t_\t_\t_\n" %(str(num+1), token, token)

				CoNLL_lines += "\n"
				fn.write(CoNLL_lines)
	
	if compress == True:
		# Compress the file and remove the text file
		archive_base =  os.path.basename(os.path.splitext(target_fn)[0]) + ".gz"
		target_base = os.path.basename(target_fn)
		target_dir = os.path.dirname(target_fn)
		call = "cd %s; tar zcvf %s %s; rm %s" % (target_dir, archive_base, target_base, target_base)
		subprocess.call([call], shell=True)

	
if __name__ == "__main__":

	# The to be parsed file
	input_fn = '../data-test/translations/test-translations-part%s.txt'

	# The pre-processed file
	output_fn = '../data-test/pre-parse/test-translations-part%s.prep.txt'

	# Go!
	for i in range(1, 6):
		prepare_parse(input_fn % i, output_fn % i)