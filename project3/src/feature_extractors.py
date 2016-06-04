
def get_art_feature(morph, head_morph):
	# head_morph  = "|".join(head_morph.split("|")[:3])
	equals = []
	head_morph = head_morph.split("|")[:3]
	morph = morph.split("|")[:3]
	for part1, part2 in zip(morph, head_morph):
		equals.append(int(part1 == part2))
	
	equals = [0,0,0] if len(equals) < 3 else equals
	return equals

def get_prep_feature(morph, head_word):
	return (head_word, morph[:3])

def get_es_feature(word, morph, head_word):
	if word == 'es' and morph[:3] == 'nom':
		return ('es', head_word)
	return False

def get_eine_feature(word_form, head_word, head_morph):
	if word_form in ['eine', 'die'] and head_morph[4:6] == 'pl':
		if head_word[-2:] in ['er', 'en']:
			feature = (word_form, head_word[-2:])
		elif head_word[-1] in ['e', 'n', 'r', 's']:
			feature = (word_form, head_word[-1:])
		else:
			feature = (word_form, 'NONE')
		return feature
		
	return False
