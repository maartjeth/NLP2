class LingFeatures:

	def __init__(self):
		self.feature_dict = {} # dict with all features and corresponding positions
		self.no_features = 0
		self.used_features = ""

	def preprocess_parse(self, parsed_file):
		with open(parsed_file, 'r') as parsed_f:
			tokens = []
			while True:
				try:
					line = parsed_f.next()
				except StopIteration: break

				if line != '\n':
					# can do this all in once, for clarity now like thgit is
					split_line = line.replace("\n", "").split("\t")
					word_id = split_line[0]
					word_form = split_line[1]
					lemma = split_line[3]
					pos_tag = split_line[5]
					morph = split_line[7]
					head = split_line[9]

					parse_dict = {
						'word_id': word_id,
						'word_form': word_form,
						'lemma': lemma,
						'pos_tag': pos_tag,
						'morph': morph,
						'head': head
						}
					tokens.append(parse_dict)
					

				else:
					yield tokens
					tokens = []
	

	def make_feature_dict(self, candidate, candidate_no):

		# 1) Find all bigrams
		#final_word_pos = candidate[-1]['word_id']
		
		for word_dict in candidate:
			pos_tag = word_dict['pos_tag']
			head = int(word_dict['head'])

			# word with word_id of head is your head and that is position head-1 in the list (as word id count starts at 1)
			pos_tag_head = candidate[head-1]['pos_tag']
			bigram_feature = '%s %s' %(pos_tag_head, pos_tag)
						
			if bigram_feature not in self.feature_dict:
				self.feature_dict[bigram_feature] = self.no_features
				self.used_features += ' %s' %str(self.no_features)				
				self.no_features += 1
			else:				
				self.used_features += ' %s' % str(self.feature_dict[bigram_feature])

		self.used_features += '\n'
		print self.used_features

	def make_features(self, feature_file):
		with open(feature_file, 'r') as feature_f:
			while True: # CHANGE
				features = line.next()




LF = LingFeatures()
feature_file = '../output/translation.1.parse'

candidate_no = 0
for candidate in LF.preprocess_parse(feature_file):
	print 'new candidate'
	LF.make_feature_dict(candidate, candidate_no)

