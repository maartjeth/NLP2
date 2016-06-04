from Model import *

# Load validatoin sentnece
val_sentences = json.load(open('../data-dev/val-sentences.json','r'))
val_sentences = [s['sentence'] for s in val_sentences]

## Generate the targets
# targets = open("../data-dev/val-targets.txt",'w')
# with open('../data/nlp2-dev.de', 'r') as file:
# 	for i, line in enumerate(file):
# 		if i in val_sentences:
# 			targets.write(line)
# targets.close()

for sample_size in [5]:#,20,40,60,80,100]
	print "-=" * 20 + '-'
	print "Starting sample size", sample_size
	print

	samples_fn = "../data-dev/samples/val-samples-{size}.txt".format(size=sample_size)
	model_name = "val-sample-size-%s" % sample_size

	M = Model(model_name, kind="dev", sample_size=sample_size, 
		features=['def'], samples_fn=samples_fn)
	M.generate_training_instances()
	M.fit()
	# M.load()
	exclude = [i for i in range(len(M.get_sentences())) if i not in val_sentences]
	M.rerank("results", exclude=exclude)
	M.write_log()
 