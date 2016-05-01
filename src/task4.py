# task 4
from collections import defaultdict

def find_best_translations(n_best_der):
	"""
	Input file (n_best_der) should look like this:

	-0.1545444841 	le chien noir 	le |1-1| chien noir |2-3|
	-0.1545444841 	un chien noir 	un |1-1| chien noir |2-3|
	-0.1529469453 	le noirs chien 	le |1-1| noirs |2-2| chien |3-3|
	-0.1529469453 	le noir chien 	le |1-1| noir |2-2| chien |3-3|
	-0.1529469453 	un noir chien 	un |1-1| noir |2-2| chien |3-3|
	""" 

	# store all translations to dict
	trans_dict = defaultdict(list)
	with open(n_best_der) as f:
		line = f.readlines()
		for phrase in line:
			parts = phrase.split('\t')
			weight = parts[0]
			trans = parts[1]
			der = parts[2]
		
			trans_dict[trans].append((weight, der))

	# Compute largest weights
	weight = 0.0
	max_weight = -float('inf')
	best_trans = ""
	best_der = ""
	for trans, weight_der in trans_dict.iteritems():
		for i in weight_der:
			weight += float(i[0])
			if weight > max_weight:
				max_weight = weight
				best_trans = trans
				best_der = i[1]

	return max_weight, best_trans, best_der

def make_output_task4(max_weight, best_trans, best_der)


if __name__ == '__main__':
	best_der = '../dummydata/blackdog-trans-der-weight'
	max_weight, best_trans, best_der = find_best_translations(best_der)

