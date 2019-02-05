from nltk.corpus import sentiwordnet as swn
def superNaiveSentiment(review):
	reviewPolarity = 0.0
	numExceptions=0
	
	for word in review.lower().split():
		weight =  0.0
		try:
			common_meaning = list(swn.senti_synsets(word))[0]

			if common_meaning.pos_score()>common_meaning.neg_score():
				weight = weight + common_meaning.pos_score()
			elif common_meaning.pos_score()<common_meaning.neg_score():
				weight = weight - common_meaning.neg_score()
		except:
			numExceptions = numExceptions +1
		reviewPolarity = reviewPolarity + weight

	return reviewPolarity

print(superNaiveSentiment("I love this product"))