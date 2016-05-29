# def test2(mylist):
# 	test(*mylist)

# def test(*args, **kwargs):
# 	print args

# test2([1,2,3,3])
# # test(1,2,3,4,5, test=1, bla=2)
# # 
# # 
# C = DefCandidateFeatures( ... )
# for candidate1, candidate2 in C:
# 	print candidate1 == [feat_val1, feat_val2, featval3, ...]
# 	# True! 
# 	# 

# S = CandidateScores( ... )
# for score1, score2 in S:
# 	METEOR score candidate1 en meteor van cand 2

# for features in zip(C, S, ...):
# 	.... 

def generate_ling_features():
	with open('blabla.postag', 'r') as file:
		for sentence in sentences: # sentences is some iterable with len=all sentences

			line = file.next()
			words = []

			while line != "": # of "\n"
				head1, head2, _, _, ... = line.replace("\n", "").split("\t")
				words.append({
					'head1': ...,
					'head2': ...
				})

			# Process words.
			# ...
			
			yield words

# Loop through all candidates
for candidate in generate_ling_features():
	# ...


