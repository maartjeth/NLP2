#!/bin/sh

java -cp ../mate/anna-3.61.jar is2.lemmatizer.Lemmatizer -model ../mate/lemma-ger-3.6.model -test ../parse/parse_input -out ../parse/parse_output_lem
java -cp ../mate/anna-3.61.jar is2.tag.Tagger -model ../mate/tag-ger-3.6.model -test ../parse/parse_output_lem -out ../parse/parse_output_postag
java -cp ../mate/anna-3.61.jar is2.mtag.Tagger -model ../mate/morphology-ger-3.6.model -test ../parse/parse_output_postag -out ../parse/parse_output_mtag
java -cp ../mate/anna-3.61.jar is2.parser.Parser -model  ../mate/parser-ger-3.6.model -test ../parse/parse_output_mtag -out ../parse/parse_output_parse