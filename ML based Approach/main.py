import nltk
with open("pos.txt",'r') as f:
	positiveReviews = f.readlines()
with open("neg.txt",'r') as f:
	negetiveReviews = f.readlines()

testTrainingSplitIndex = 3500;

testNegativeReviews = negetiveReviews[testTrainingSplitIndex+1:]
testPositiveReviews = positiveReviews[testTrainingSplitIndex+1:]

trainingNegativeReviews = negetiveReviews[:testTrainingSplitIndex]
trainingPositiveReviews = positiveReviews[:testTrainingSplitIndex]

def getVocabulary():
	#Creating list for all the words present in positive reviews
	positiveWordList = [word for line in trainingPositiveReviews for word in line.split()]
	#Creating list for all the words present in Negative reviews
	negativeWordList = [word for line in trainingNegativeReviews for word in line.split()]
	#Combining the above list
	allWordList = [item for sublist in [positiveWordList,negativeWordList] for item in sublist]
	allWordSet = list(set(allWordList))
	return allWordList

def extract_feature(review):
	review_words=set(review)
	features={}
	for word in getVocabulary() :
		features[word] = (word in review_words)
	return features

def getTrainingData():
	negTaggedTrainingReviewList = [{ 'review':oneReview.split(),'label':'negative'} for oneReview in trainingNegativeReviews]
	posTaggedTrainingReviewList = [{ 'review':oneReview.split(),'label':'positive'} for oneReview in trainingPositiveReviews]

	fullTaggedTrainingReviewData = [item for sublist in [negTaggedTrainingReviewList,posTaggedTrainingReviewList] for item in sublist]
	trainingData = [(review['review'],review['label']) for review in fullTaggedTrainingReviewData]
	return trainingData

def getTrainedNaiveBayesClassifier(extract_feature, trainingData):
	trainingFeatures = nltk.classify.apply_features(extract_feature, trainingData)
	trainedNBClassifier = nltk.NaiveBayesClassifier.train(trainingFeatures)
	return trainedNBClassifier

# trainedNBClassifier = getTrainedNaiveBayesClassifier(extract_feature, trainingData)

def naiveBayesSentimentCalculator(review):
	problemInstance = review.split()
	problemFeatures = extract_feature(problemInstance)
	trainingData = getTrainingData()
	trainedNBClassifier = getTrainedNaiveBayesClassifier(extract_feature, trainingData)
	return trainedNBClassifier.classify(problemFeatures)

def getTestReviewSentiments(naiveBayesSentimentCalculator):
	testNegResults = [naiveBayesSentimentCalculator(review) for review in testNegativeReviews]
	testPosResults = [naiveBayesSentimentCalculator(review) for review in testPositiveReviews]
	labelToNum = {'positive':1,'negative':-1}
	numericNegResults = [labelToNum[x] for x in testNegResults]
	numericPosResults = [labelToNum[x] for x in testPosResults]
	return {'results-on-positive':numericPosResults, 'results-on-negative':numericNegResults}

def runDiagnostics(reviewResults):
	positiveReviewsResult = reviewResult['results-on-positive']
	negetiveReviewsResult = reviewResult['results-on-negative']
	numTruePositive = sum(x>0 for x in positiveReviewsResult)
	numTrueNegative = sum(x<0 for x in negativeReviewsResult)
	pctTruePositive = float(numTruePositive)/len(positiveReviewsResult)
	pctTrueNegative = float(numTrueNegative)/len(negativeReviewsResult)
	total = len(positiveReviewsResult) + len(negativeReviewsResult)
	totalAccurate = numTruePositive + numTrueNegative
	print("Accuracy on positive reviews = " + "%.2f" %(pctTruePositive*100) + "%")
	print("Accuracy on negative reviews = " + "%.2f" %(pctTrueNegative*100) + "%")
	print("Overall accuracy = " + "%.2f" %(totalAccurate*100/total) + "%")


#to use this classifier comment out the below line
#naiveBayesSentimentCalculator("Your review")

#to ckeck the accuracy 
runDiagnostics(getTestReviewSentiments(naiveBayesSentimentCalculator))