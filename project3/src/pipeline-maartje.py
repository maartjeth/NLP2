from Model import *

all_features = 'def bigrams tags artpl es prep prepart art wordcount ratio def-combined'.split()

def run_model_without_features(wo_features, name):
	features = [f for f in all_features if f not in wo_features]
	model = Model(name, kind="dev", sample_size=40, features=features)
	model.generate_training_instances()
	model.fit()
	model.rerank("results")
	model.write_log()

# WITHOUT TAGS
run_model_without_features(['tag'], 'wo_unigram')

# WITHOUT GRAMMAR
wo_features = 'artpl es prep prepart art wordcount ratio'.split()
run_model_without_features(wo_features, 'wo_grammar')

