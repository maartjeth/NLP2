import json

class LingFeatures:

	def __init__(self, sentences):
		self.feature_dict = {} # dict with all features and corresponding positions - starting with some known once
		self.no_features = 0
		self.used_features = ""
		self.sentences = sentences

		# TODO: this is a dict without the words with non-ascii characters, find out how to include them:
		# chosen for a dict as then the look-up  time is O(1) instead of O(n), although it's a bit strange with 'NONE'
		self.preps = {
			'mit': None,
			'nach': None,
			'bei': None,
			'seit': None,
			'von': None,
			'zu': None,
			'aus': None,
			'ausser': None,
			'an': None,
			'auf': None,
			'hinter': None,
			'neben': None,
			'in': None,
			'unter': None,
			'vor': None,
			'zwischen': None,
			'durch': None,
			'ohne': None,
			'um': None,
			'entlang': None,
			'bis': None,
			'gegen': None
		}

		self.articles = {
			'die': None,
			'des': None,
			'dem': None,
			'den': None,
			'der': None,
			'das': None,
		}

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
		""" Make a dictionary with all features you encounter and save all
		the features to a file, so that you in the end you only need to 

		"""

		#final_word_pos = candidate[-1]['word_id']
		my_preps = {}
		for word_dict in candidate:
			# 1) Find all bigrams
			pos_tag = word_dict['pos_tag']
			head = int(word_dict['head']) 
			word_id = word_dict['word_id']

			# root + next tag (do we want to include end of line? if so, how?)
			if head == 0:
				bigram_feature = '%s %s' %('root', pos_tag)
				
			else:
				# word with word_id of head is your head and that is position head-1 in the list (as word id count starts at 1)
				pos_tag_head = candidate[head-1]['pos_tag']
				bigram_feature = '%s %s' %(pos_tag_head, pos_tag)
			
			self.put_in_feature_dict(bigram_feature)
			
			## SO THIS DOESNT WORK ANYMORE
			# 2) Find linguistic features
			# 2.1) Prepositions (prep + article: no use to use nouns, as the pos tagger tags based on the article...)
			word_form = word_dict['word_form']
			head_word = candidate[head-1]['word_form']
			if head_word in self.preps and word_form in self.articles:
				prep_feature = '%s %s' %(head_word, word_dict['morph'][0:3]) # first 3 letters are the case, which is important
				#prep_feature = '%s %s' %(head_word, word_form)
				self.put_in_feature_dict(prep_feature)
				print prep_feature

			# 2.2) Articles
			# check whether the correct article is used for the noun 
			if word_form in self.articles:
				art_feature = '%s %s' %(word_form, candidate[head-1]['morph']) # all features are important here
				self.put_in_feature_dict(art_feature)
				#print art_feature





		self.used_features += '\n'

	def put_in_feature_dict(self, feature):
		# check whether feature in feature dict, if not add, else, just append to used features			
		if feature not in self.feature_dict:
			self.feature_dict[feature] = self.no_features
			# guess we shouldnt use a string!!!
			self.used_features += ' %s' %str(self.no_features) # use this to write all features used in the sentence to a file, so that you can retrieve all features per sentence later 				
			self.no_features += 1
		else:				
			self.used_features += ' %s' % str(self.feature_dict[feature])

	def write_features_to_file(self, all_features_file):
		with open(all_features_file, 'a') as f:
			f.write(self.used_features)



feature_file = '../output/translation.1.parse'
#feature_file = '../data/data-dev/parse/dev-part1.parse/dev-part1.parse'
sentences_fn = '../data/data-dev/dev-sentences.json'
all_features_file = '../output/TEST.txt'
#all_features_file = '../output/all_ling_features.txt'

sentences = json.load(open(sentences_fn))
LF = LingFeatures(sentences)

s = 0
candidate_no = 0
for candidate in LF.preprocess_parse(feature_file):
	#print candidate_no
	LF.make_feature_dict(candidate, candidate_no)
	if sentences[s]['num_candidates'] == candidate_no:
		LF.write_features_to_file(all_features_file)
		s += 1
		print s
		candidate_no = 0
	else:
		candidate_no += 1

print LF.used_features

