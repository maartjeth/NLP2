from Model import *

all_features = 'def bigram tag artpl es prep prepart art wordcount ratios def-combined'.split()

sep = ("*"*80+"\n")*3

def run_model_separated_95(wo_features, name):
	try: 
		samples_fn = "../data-dev/samples/dev-samples-40-separated-100-95.txt"
		pro_scores_fn = "../data-dev/dev-meteor-95.txt"
		features = [f for f in all_features if f not in wo_features]
		model = Model(name, kind="dev", sample_size=40, features=features, 
			samples_fn=samples_fn, pro_scores_fn=pro_scores_fn)
		model.generate_training_instances()
		model.fit()
		model.rerank("results")
		model.write_log()
	except: 
		print "SOME ERROR OCCURED, CONTINUING..."
		pass


# print sep, "BASELINE MODEL with only DEF with SEPARATED SAMPLES, alpha=95"
# wo_features = [f for f in all_features if f != "def"]
# run_model_separated_95(wo_features, 'def_sep_samples_95')

print sep, "FULL MODEL with SEPARATED SAMPLES, alpha=95"
run_model_separated_95(['def'], 'full_sep_samples_95')

print sep, "FULL MODEL without COMBINED with SEPARATED SAMPLES, alpha=95"
run_model_separated_95(['def-combined'], 'wo_combined_sep_samples_95')

# Maartje:
# print sep, "FULL MODEL without UNIGRAM with SEPARATED SAMPLES, alpha=95"
# run_model_separated_95(['def', 'tag'], 'wo_unigram_sep_samples_95')

print sep, "FULL MODEL without GRAMMAR with SEPARATED SAMPLES, alpha=95"
wo_features = 'def artpl es prep prepart art wordcount ratios'.split()
run_model_separated_95(wo_features, 'wo_grammar_sep_samples_95')

# Maartje doet ook:
print sep, "FULL MODEL without BIGRAM with SEPARATED SAMPLES, alpha=95"
run_model_separated_95(['def', 'bigram'], 'wo_bigram_sep_samples_95')

