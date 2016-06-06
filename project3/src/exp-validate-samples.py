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

# for sample_size in [5,20,40,60,80,100]:
# 	print "-=" * 20 + '-'
# 	print "Starting sample size", sample_size
# 	print

# 	samples_fn = "../data-dev/samples/val-samples-{size}-3.txt".format(size=sample_size)
# 	model_name = "val-sample-size-%s-3" % sample_size

# 	M = Model(model_name, kind="dev", sample_size=sample_size, 
# 		features=['def'], samples_fn=samples_fn)
# 	M.generate_training_instances()
# 	M.fit()
# 	M.load()
# 	exclude = [i for i in range(len(M.get_sentences())) if i not in val_sentences]
# 	M.rerank("results", exclude=exclude, kind="dev")
# 	M.write_log()
# 	

sample_size = 100
for run in [1, 2, 3]:
	samples_fn = "../data-dev/samples/val-samples-{size}-{run}.txt".format(size=sample_size,run=run)
	pro_scores_fn = "../data-dev/dev-meteor-05.txt"
	M = Model("val-meteor-05-"+str(run), 
		kind="dev", sample_size=sample_size, 
		features=['def'], samples_fn=samples_fn, pro_scores_fn=pro_scores_fn)
	M.generate_training_instances()
	M.fit()
	M.load()
	exclude = [i for i in range(len(M.get_sentences())) if i not in val_sentences]
	M.rerank("results", exclude=exclude, kind="dev")
	M.write_log()

 

 # Len def_featres: 12185