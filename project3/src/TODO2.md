* Features test set berekenen: alleen nog combined ('bijna' klaar)
* Pipeline voor alle experimenten schrijven
	--> splitsen 
* multeval fixen
* iets schrijven

# MODELS:
* `baseline`: default features and weights from `baseline.weights`
* `ranked-baseline`: default features, but with new weights (and ranking)
* `full`: all features
* `full-bigram`: all features except `bigram`
* `full-unigram`: all features except `tags`
* `full-grammar`: all features except `artpl`, `es`, `prep`, `prepart`, `art`, `wordcount`, `ratio`
* `full-combined`: all features except `def-combined`

* KLAAR: default features uitschrijven test / dev --> handig; misschien 15min?
* KLAAR: validation experiments: 1u
* KLAAR: Combined features opnieuw, met linebreaks: < 60min. 
* pipeline schrijven: 1min
* 