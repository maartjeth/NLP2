from Helper import *
import subprocess

def prep_parse_files(self):

	for s, candidates in H.read_1000best(first=1, last=2):
		# every i is an instance of a candidate (i.e. 1000 i's for every candidate)
		# for every s you want to make a new file
		#if s == '1': # for debugging
		filename = self.settings['parse_dir']+"%s%s" %("parse_input", s)
		with open(filename, 'w') as fn:
			for i, candidate in enumerate(candidates):
				CoNLL_lines = ""
				#if i == 0 or i == 1 or i == 890: # for debugging
				translation = candidate['translation_sent'].split()
				for num, token in enumerate(translation):
					CoNLL_lines += "%s\t%s\t%s\t_\t_\t_\t_\t_\t_\t_\t_\t_\t_\n" %(str(num+1), token, token)

				CoNLL_lines += "\n"
				fn.write(CoNLL_lines)

def parse_pipeline(self, steps, num_files):
	""" Parsing pipe line according to the mate parsing: 
		(0) lemmatization
		(1) pos tagging
		(2) morphological tagging
		(3) parsing

		Input: 
		steps - add a list with numbers of the pipeline that you want to execute
		num_files - how many files do you want to parse?

	"""

	for i in steps:
		if i == 0:
			# do lemmatization
			# java -cp ../mate/anna-3.61.jar is2.lemmatizer.Lemmatizer -model ../mate/lemma-ger-3.6.model -test ../parse/parse_input1 -out ../parse/test1.output
			for s in range(num_files):
				input_file = self.settings['parse_dir']+"%s%s" %("parse_input", s+1)
				print input_file
				output_file = self.settings['parse_dir']+"%s%s" %("parse_output_lem", s+1)
				print output_file
				call = "java -cp ../mate/anna-3.61.jar is2.%s -model %s -test %s -out %s" %("lemmatizer.Lemmatizer", "../mate/lemma-ger-3.6.model", input_file, output_file)
				print call
				subprocess.call([call], shell=True)
				print 'subprocess ended'

		if i == 1:
			# do pos tagging
			# java -cp anna-3.61.jar is2.tag.Tagger -model tag-ger-3.6.model -test test1.output -out test2.output
			for s in range(num_files):
				input_file = self.settings['parse_dir']+"%s%s" %("parse_output_lem", s+1)
				output_file = self.settings['parse_dir']+"%s%s" %("parse_output_postag", s+1)
				call = "java -cp ../mate/anna-3.61.jar is2.%s -model %s -test %s -out %s" %("tag.Tagger", "../mate/tag-ger-3.6.model", input_file, output_file)
				print call
				subprocess.call([call], shell=True)

		if i == 2:
			# do morphological tagging
			#java -cp anna-3.61.jar is2.mtag.Tagger -model morphology-ger-3.6.model -test test2.output -out test3.output
			for s in range(num_files):
				input_file = self.settings['parse_dir']+"%s%s" %("parse_output_postag", s+1)
				output_file = self.settings['parse_dir']+"%s%s" %("parse_output_mtag", s+1)
				call = "java -cp ../mate/anna-3.61.jar is2.%s -model %s -test %s -out %s" %("mtag.Tagger", "../mate/morphology-ger-3.6.model", input_file, output_file)
				print call
				subprocess.call([call], shell=True)

		if i == 3:
			# do parsing
			# java -cp anna-3.61.jar is2.parser.Parser -model parser-ger-3.6.model -test test2.output -out test4.output
			for s in range(num_files):
				input_file = self.settings['parse_dir']+"%s%s" %("parse_output_mtag", s+1)
				output_file = self.settings['parse_dir']+"%s%s" %("parse_output_parse", s+1)
				call = "java -cp ../mate/anna-3.61.jar is2.%s -model %s -test %s -out %s" %("parser.Parser", " ../mate/parser-ger-3.6.model", input_file, output_file)
				print call
				subprocess.call([call], shell=True)


Helper.prep_parse_files = prep_parse_files
Helper.parse_pipeline = parse_pipeline

if __name__ == '__main__':
	H = Helper()
	#H.prep_parse_files()
	H.parse_pipeline([0, 1, 2, 3], 1)
	#H.parse_pipeline([0], 1)