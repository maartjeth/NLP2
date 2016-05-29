#!/bin/bash

# The "name" of this run. This can be "demo" or e.g. "part4"
name="demo"

# dev/test
kind="dev"

# The root directory
root=~/Github\ Projects/NLP2/project3

# Where to save the whole lot?
output_dir="data-dev/parse/"

###############################################################

# Mate and Mate models
mate="libraries/mate/anna-3.61.jar"
model_lemma="libraries/mate/lemma-ger-3.6.model"
model_tag="libraries/mate/tag-ger-3.6.model"
model_morph="libraries/mate/morphology-ger-3.6.model"
model_parse="libraries/mate/parser-ger-3.6.model"


# output files
output_base="$output_dir/parse-$name"
output_lemma_fn="$output_base.lem"
output_postag_fn="$output_base.postag"
output_morph_fn="$output_base.morph"
output_parse_fn="$output_base.parse"

# Pre-processed files
pre_parse_dir="data-$kind/pre-parse"
archive_fn="$kind-$name.gz"

#############################################################

echo "**************************************************"
echo "* PARSING SCRIPT"
echo "* Kind: $kind"
echo "* Name: $name"
echo "* Parsing: $pre_parse_dir/$acrhive_fn"
echo "*"


# Extract the archive and get the txt file name
echo 'Extracting pre-processed file...'
cd "$root"
cd "$pre_parse_dir"
input_fn="$pre_parse_dir/$(tar tzf $archive_fn)"
tar zxvf $archive_fn
cd "$root"

# Go, go, go!
echo 'Starting...'
java -Xmx3G -cp $mate is2.lemmatizer.Lemmatizer -model $model_lemma -test $input_fn -out $output_lemma_fn -Xmx4000m
java -Xmx3G -cp $mate is2.tag.Tagger -model $model_tag -test $output_lemma_fn -out $output_postag_fn
java -Xmx3G -cp $mate is2.mtag.Tagger -model $model_morph -test $output_postag_fn -out $output_morph_fn
java -Xmx3G -cp $mate is2.parser.Parser -model  $model_parse -test $output_morph_fn -out $output_parse_fn
echo 'Done parsing!'

echo "Cleaning up unpacked archives..."
cd "$root"
rm $input_fn

# For multiple parts, use this:
#for i in {1..1}
#do
	#...
#done