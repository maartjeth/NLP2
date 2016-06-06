from Model import *

all_features = 'def bigram tag artpl es prep prepart art wordcount ratios def-combined'.split()

sep = ("*"*80+"\n")*3

def run_model_without_features(wo_features, name):
	try:
		features = [f for f in all_features if f not in wo_features]
		model = Model(name, kind="dev", sample_size=40, features=features)
		model.generate_training_instances()
		model.fit()
		model.rerank("results")
		model.write_log()
	except: 
		print "SOME ERROR OCCURED, CONTINUING..."
		pass

def run_model_without_features_separated(wo_features, name):
	try: 
		samples_fn = "../data-dev/samples/dev-samples-40-separated-100.txt"
		features = [f for f in all_features if f not in wo_features]
		model = Model(name, kind="dev", sample_size=40, features=features, samples_fn=samples_fn)
		model.generate_training_instances()
		model.fit()
		model.rerank("results")
		model.write_log()
	except: 
		print "SOME ERROR OCCURED, CONTINUING..."
		pass


# print sep, "BASELINE MODEL with only DEF with SEPARATED SAMPLES"
# wo_features = [f for f in all_features if f != "def"]
# run_model_without_features_separated(wo_features, 'def_sep_samples')

# print sep, "FULL MODEL with SEPARATED SAMPLES"
# run_model_without_features_separated(['def'], 'full_sep_samples')

# print sep, "FULL MODEL without BIGRAM with SEPARATED SAMPLES"
# run_model_without_features_separated(['def', 'bigram'], 'wo_bigram_sep_samples')

# MAARTJE:

# print sep, "FULL MODEL without UNIGRAM with SEPARATED SAMPLES"
# run_model_without_features_separated(['def', 'unigram'], 'wo_unigram_sep_samples')

# print sep, "FULL MODEL without COMBINED with SEPARATED SAMPLES"
# run_model_without_features_separated(['def-combined'], 'wo_combined_sep_samples')

# print sep, "FULL MODEL without GRAMMAR with SEPARATED SAMPLES"
# wo_features = 'def artpl es prep prepart art wordcount ratios'.split()
# run_model_without_features_separated(wo_features, 'wo_grammar_sep_samples')


# print sep, "BASELINE MODEL with only DEF"
# wo_features = [f for f in all_features if f != "def"]
# run_model_without_features(wo_features, 'def')

# print sep, "FULL MODEL"
# run_model_without_features(['def'], 'full')

# print sep, "FULL MODEL without BIGRAM"
# run_model_without_features(['def', 'bigram'], 'wo_bigram')
# 

print sep, "FULL MODEL without GRAMMAR with SEPARATED SAMPLES"
wo_features = 'def artpl es prep prepart art wordcount ratios'.split()
run_model_without_features_separated(wo_features, 'wo_grammar_sep_samples')

wo_features1 = [f for f in all_features if f not in ["def", "tag"]]
print sep, "CORE FEATURES and UNIGRAM with SEPARATED SAMPLES"
run_model_without_features_separated(wo_features1, 'only_unigram_sep_samples')

print sep, "FULL MODEL without UNIGRAM"
run_model_without_features(['def', 'tag'], 'wo_unigram')

print sep, "FULL MODEL without COMBINED"
run_model_without_features(['def-combined'], 'wo_def_combined')

print sep, "FULL MODEL without LINGUISTIC"
wo_features2 = 'def artpl es prep prepart art wordcount ratios'.split()
run_model_without_features(wo_features2, 'wo_grammar')
