from Model import *

all_features = 'def bigram tag artpl es prep prepart art wordcount ratios def-combined'.split()

def run_model_without_features(wo_features, name):
	try:
		features = [f for f in all_features if f not in wo_features]
		model = Model(name, kind="dev", sample_size=40, features=features)
		model.generate_training_instances()
		model.fit()
		model.rerank("results")
		model.write_log()
	except: pass

def run_model_without_features_separated(wo_features, name):
	try: 
		samples_fn = "../data-dev/samples/dev-samples-40-separated-100.txt"
		features = [f for f in all_features if f not in wo_features]
		model = Model(name, kind="dev", sample_size=40, features=features, samples_fn=samples_fn)
		model.generate_training_instances()
		model.fit()
		model.rerank("results")
		model.write_log()
	except: pass


sep = ("*"*80+"\n")*3

# TEST MODEL
print sep, "A test..."
model = Model('test', kind="dev", sample_size=1, features=['def'])
model.generate_training_instances()
model.fit()
exclude = [i for i in range(len(model.get_sentences())) if i > 100]
model.rerank("results", exclude=exclude, kind="dev")
model.write_log()


# FULL MODEL
# print sep, "FULL MODEL"
# model = Model('full', kind="dev", sample_size=40, features=all_features)
# model.load()
# model.rerank("results")
# model.write_log()
# run_model_without_features([], 'full')

# # WITHOUT COMBINED
# # run_model_without_features(['def-combined'], 'wo_combined')

# # WITHOUT BIGRAM
# print sep, "WO BIGRAM"
# run_model_without_features(['bigram'], 'wo_bigram')

# WITHOUT RATIO
# print sep, "WITHOUT RATIOS"
# wo_features = ['ratios']
# run_model_without_features(wo_features, 'wo_ratios')

# WITHOUT WORDCOUNTS
# print sep, "WITHOUT WORDCOUNTS"
# wo_features = ['wordcounts']
# run_model_without_features(wo_features, 'wo_wordcounts')

# WITHOUT GRAMMAR_THINGS
# print sep, "WITHOUT GRAMMAR SPARSE"
# wo_features = 'artpl es prep prepart art'.split()
# run_model_without_features(wo_features, 'wo_grammar_sparse')

# print sep, "WITHOUT GRAMMAR"
# wo_features = 'artpl es prep prepart art wordcount ratios'.split()
# run_model_without_features(wo_features, 'wo_grammar')

# print sep, "ONLY DEF"
# wo_features = [f for f in all_features if f != "def"]
# run_model_without_features(wo_features, 'def')

# print sep, "DEF SEPARATED SAMPLING"
# sample_size = 1000
# samples_fn = "../data-dev/samples/dev-samples-{size}-separated-500.txt".format(size=sample_size)
# model = Model('def-sep-samples-1000', kind="dev", sample_size=sample_size, features=['def'], samples_fn=samples_fn)
# model.generate_training_instances()
# model.fit()
# model.rerank("results")
# model.write_log()

print sep, "FULL SEPERATED SAMPLES"
run_model_without_features_separated(['def'], 'full_sep_samples')

# print sep, "WITHOUT COMBINED SEPARATED SAMPLES"
# run_model_without_features_separated(['def-combined'], 'wo_combined_sep_samples')

# print sep, "WO BIGRAM SEPARATED SAMPLES"
# run_model_without_features(['bigram'], 'wo_bigram_sep_samples')
