from Model import *

all_features = 'def bigrams tags artpl es prep prepart art wordcount ratio def-combined'.split()

def run_model_without_features(wo_features, name):
	features = [f for f in all_features if f not in wo_features]
	model = Model(name, kind="dev", sample_size=40, features=features)
	model.generate_training_instances()
	model.fit()
	model.rerank("results")
	model.write_log()

sep = ("*"*80+"\n")*3

# TEST MODEL
print sep, "A test..."
model = Model('test', kind="dev", sample_size=1, features=['def'])
model.generate_training_instances()
model.fit()
exclude = [i for i in range(len(model.get_sentences())) if i > 100]
model.rerank("results", exclude=exclude, kind="dev")
model.write_log()


# # FULL MODEL
print sep
# run_model_without_features([], 'full')

# # WITHOUT COMBINED
# # run_model_without_features(['def-combined'], 'wo_combined')

# # WITHOUT BIGRAM
print sep
# run_model_without_features(['bigram'], 'wo_bigram')
