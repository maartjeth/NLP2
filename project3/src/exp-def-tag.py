from Model import *


M = Model("test-def-tag-bigram", kind="dev", sample_size=100, features=['def','tag', 'bigram'])
M.generate_training_instances()
M.fit()
# M.load()
# exclude = [i for i in range(len(M.sentences)) if i not in val_sentences]
# M.rerank("results", exclude=exclude)
M.write_log()
