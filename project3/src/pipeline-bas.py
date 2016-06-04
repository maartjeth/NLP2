from Model import *

all_features = 'def bigrams tags artpl es prep prepart art wordcount ratio def-combined'.split()

def run_model_without_features(wo_features, name):
	features = [f for f in all_features if f not in wo_features]
	model = Model(name, kind="dev", sample_size=40, features=features)
	model.generate_training_instances()
	model.fit()
	model.rerank("results")
	model.write_log()

# FULL MODEL
run_model_without_features([], 'full')

# WITHOUT COMBINED
# run_model_without_features(['def-combined'], 'wo_combined')

# WITHOUT BIGRAM
run_model_without_features(['bigram'], 'wo_bigram')
