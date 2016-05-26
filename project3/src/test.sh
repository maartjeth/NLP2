#!/bin/bash
root="/nlp-intermediates"
output_dir="../output"
mate="../mate/anna-3.61.jar"
model_lemma="../mate/lemma-ger-3.6.model"
model_tag="../mate/tag-ger-3.6.model"
model_morph="../mate/morphology-ger-3.6.model"
model_parse="../mate/parser-ger-3.6.model"

# CHANGE THIS!
for i in {1..1}
do
	input_fn="${root}/translations-test.prep.$i.txt"
	output_base="${output_dir}/translation.$i"
	output_lemma_fn="${output_base}.lem"
	output_postag_fn="${output_base}.postag"
	output_morph_fn="${output_base}.morph"
	output_parse_fn="${output_base}.parse"
	
   	# Go, go, go!
	java -cp $mate is2.lemmatizer.Lemmatizer -model $model_lemma -test $input_fn -out $output_lemma_fn -Xmx4000m
	java -cp $mate is2.tag.Tagger -model $model_tag -test $output_lemma_fn -out $output_postag_fn
	java -cp $mate is2.mtag.Tagger -model $model_morph -test $output_postag_fn -out $output_morph_fn
	java -cp $mate is2.parser.Parser -model  $model_parse -test $output_morph_fn -out $output_parse_fn
done