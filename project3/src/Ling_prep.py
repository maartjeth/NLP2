from Helper import *

def prep_parse_files(self):

	for s, candidates in H.read_1000best(first=1, last=2):
		# every i is an instance of a candidate (i.e. 1000 i's for every candidate)
		# for every s you want to make a new file
		if s == '1': # for debugging
			filename = self.settings['parse_dir']+"%s%s" %("parse_input", s)
			with open(filename, 'w') as fn:
				for i, candidate in enumerate(candidates):
					CoNLL_lines = ""
					if i == 0 or i == 1 or i == 890: # for debugging
						translation = candidate['translation_sent'].split()
						for num, token in enumerate(translation):
							CoNLL_lines += "%s \t %s %s \t _ \t _ \t _ \t _ \t _ \t _ \t _ \t _ \t _ \t _ \n" %(str(num+1), token, token)

						CoNLL_lines += "\n"
						fn.write(CoNLL_lines)



Helper.prep_parse_files = prep_parse_files

if __name__ == '__main__':
	H = Helper()
	H.prep_parse_files()
