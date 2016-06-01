#!/bin/bash

### 
# Evaluates the translation candidates METEOR scores.
# 

# The "name" of this run. This can be "demo" or e.g. "part4"
name="part6"

out_dir="eval-3"

# The root directory
root=~/Github\ Projects/NLP2/project3

kind="dev"

# $params='0.05 1.0 0.55 0.55'

##################################################### 

echo "**********************************************"
echo "* Evaluate meteor scores"
echo "* Name: $name"
echo "* Kind: $kind"
echo "* Out dir: $out_dir"
echo "**"

# FIlenames
translations="data-$kind/translations/$kind-translations-$name.txt"
targets="data-$kind/eval/$kind-targets-$name.txt"
eval_results="data-$kind/$out_dir/$kind-meteor-output-$name.txt"

# Location of METEOR and the german paraphrasing model
meteor="libraries/meteor/meteor-1.5.jar"
paraphrase_de="libraries/meteor/data/paraphrase-de.gz"

# Go to root
cd "$root"
java -Xmx2G -jar $meteor $translations $targets -l de -norm -a "$paraphrase_de" \
	-p '0.05 1.0 0.55 0.55' -w "1.0 0.8 0.2" > $eval_results