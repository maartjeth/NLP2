#!/bin/bash

### 
# Evaluates the translation candidates METEOR scores.
# 

# The "name" of this run. This can be "demo" or e.g. "part4"
name="part6"

# The root directory
root=~/Github\ Projects/NLP2/project3

##################################################### 

# FIlenames
translations="data-dev/translations/dev-translations-$name.txt"
targets="data-dev/eval/dev-targets-$name.txt"
eval_results="data-dev/eval/dev-meteor-$name.txt"

# Location of METEOR and the german paraphrasing model
meteor="libraries/meteor/meteor-1.5.jar"
paraphrase_de="libraries/meteor/data/paraphrase-de.gz"

# Go to root
cd "$root"
java -Xmx2G -jar $meteor $translations $targets -l de -norm -a $paraphrase_de > $eval_results