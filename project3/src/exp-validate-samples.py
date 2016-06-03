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

for sample_size in [20]:#,15,20,40,80,100,160,320,640]:
	print "-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
	print "Starting sample size", sample_size
	print

	samples_fn = "{root}/models/{name}/val-samples-{sample_size}.txt"
	M = Model("val-sample-size-"+str(sample_size)+"-2", kind="dev", sample_size=sample_size, features=['def'], samples_fn=samples_fn)
	M.generate_training_instances()
	M.fit()
	# M.load()
	exclude = [i for i in range(len(M.sentences)) if i not in val_sentences]
	M.rerank("results", exclude=exclude)
	M.write_log()
