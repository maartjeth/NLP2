# NLP2 Project 3: Ranking translations

PARSER:

Wat moet je doen om het werkend te krijgen (staat ook in de short manual, maar hier nog shorter :) )

Alle downloads via: https://code.google.com/archive/p/mate-tools/downloads

1) Download de parser: anna-3.61.jar (niks meer aan doen :) )
2) Download de models: ger-tagger+lemmatizer+morphology+graph-based-3.6+.tgz	
3) Maak de files die je wilt parsen, met als opmaak: 
word id, word form, gold lemma, predicted lemma, gold POS, predicted POS, gold features, predicted features, gold head, predicted head, gold label, predicted label

Maak hiervan twaalf kolommen gescheiden door tabs. Als je een veld niet weet kan je het invullen met een underscore. Voorbeeld: 

1	Ich	Ich	_	_	_	_	_	_	_	_	_	_
2	bin	bin	_	_	_	_	_	_	_	_	_	_
3	alt	alt	_	_	_	_	_	_	_	_	_	_
4	.	.	_	_	_	_	_	_	_	_	_	_

Run je code via: 

Lemmatizer:
$>java -cp anna-3.3.jar is2.lemmatizer.Lemmatizer -model <modelle>
-test <inputle> -out <outputle>

POS tagger:
$>java -cp anna-3.3.jar is2.tag.Tagger -model <modelle> -test <inputle>
-out <outputle>

Morphology tagger:
$>java -cp anna-3.3.jar is2.mtag.Tagger -model <modelle> -test <inputle>
-out <outputle>

Dependency parser:
$>java -cp anna-3.3.jar is2.parser.Parser -model <modelle> -test <inputle>
-out <outputle>

Je moet alles achter elkaar runnen.
Een voorbeeld van wat ik gerund heb:

java -cp anna-3.61.jar is2.lemmatizer.Lemmatizer -model lemma-ger-3.6.model -test test_tag.test -out test1.output

java -cp anna-3.61.jar is2.tag.Tagger -model tag-ger-3.6.model -test test1.output -out test2.output

java -cp anna-3.61.jar is2.mtag.Tagger -model morphology-ger-3.6.model -test test2.output -out test3.output

java -cp anna-3.61.jar is2.parser.Parser -model parser-ger-3.6.model -test test2.output -out test4.output

En van de output die dat gaf (laatste file):

1	Ich	Ich	ich	_	PPER	_	_	-1	2	_	SB	_	_
2	bin	bin	sein	_	VAFIN	_	_	-1	0	_	--	_	_
3	alt	alt	alt	_	ADJD	_	_	-1	2	_	PD	_	_
4	.	.	--	_	$.	_	_	-1	3	_	--	_	_

Je ziet dus dat ie de kolom invult waar je naar vraagt.

Google doc met wat printscreens: 
https://docs.google.com/document/d/1AguWB3PffNGVkPgVXQIp0HrneGwjtgkXqdkWKcoSSl0/edit?usp=sharing