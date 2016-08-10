import re, math, collections, itertools, os
import nltk, nltk.classify.util, nltk.metrics
from nltk.classify import NaiveBayesClassifier
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist


CLE_WIN_FILE = 'CLEWinsCmts.txt'
RT_POLARITY_NEG_FILE = 'GSWWinsCmts.txt'


# this function takes a feature selection mechanism and returns its performance in a variety of metrics
def evaluate_features(feature_select):
	cleFeatures = []
	gswFeatures = []
	# http://stackoverflow.com/questions/367155/splitting-a-string-into-words-and-punctuation
	# breaks up the sentences into lists of individual words (as selected by the input mechanism) and appends 'pos' or 'neg' after each list
	with open(CLE_WIN_FILE, 'r') as cleSentences:
		for i in cleSentences:
			cleWords = re.findall(r"[\w']+|[.,!?;]", i.rstrip())
			cleWords = [feature_select(cleWords), 'CLE']
			cleFeatures.append(cleWords)
	with open(RT_POLARITY_NEG_FILE, 'r') as gswSentences:
		for i in gswSentences:
			gswWords = re.findall(r"[\w']+|[.,!?;]", i.rstrip())
			gswWords = [feature_select(gswWords), 'GSW']
			gswFeatures.append(gswWords)

	# selects 3/4 of the features to be used for training and 1/4 to be used for testing
	cleCutoff = int(math.floor(len(cleFeatures) * 3 / 4))
	gswCutoff = int(math.floor(len(gswFeatures) * 3 / 4))
	trainFeatures = cleFeatures[:cleCutoff] + gswFeatures[:gswCutoff]
	testFeatures = cleFeatures[cleCutoff:] + gswFeatures[gswCutoff:]

	# trains a Naive Bayes Classifier
	classifier = NaiveBayesClassifier.train(trainFeatures)

	# initiates referenceSets and testSets
	referenceSets = collections.defaultdict(set)
	testSets = collections.defaultdict(set)

	# puts correctly labeled sentences in referenceSets and the predictively labeled version in testsets
	for i, (features, label) in enumerate(testFeatures):
		referenceSets[label].add(i)
		predicted = classifier.classify(features)
		testSets[predicted].add(i)

	# prints metrics to show how well the feature selection did
	print 'train on %d instances, test on %d instances' % (len(trainFeatures), len(testFeatures))
	print 'accuracy:', nltk.classify.util.accuracy(classifier, testFeatures)
	# print 'cle precision:', nltk.metrics.precision(referenceSets['cle'], testSets['cle'])
	# print 'cle recall:', nltk.metrics.recall(referenceSets['cle'], testSets['cle'])
	# print 'gsw precision:', nltk.metrics.precision(referenceSets['gsw'], testSets['gsw'])
	# print 'gsw recall:', nltk.metrics.recall(referenceSets['gsw'], testSets['gsw'])
	classifier.show_most_informative_features(10)


# creates a feature selection mechanism that uses all words
def make_full_dict(words):
	return dict([(word, True) for word in words])


# tries using all words as the feature selection mechanism
print 'using all words as features'
evaluate_features(make_full_dict)


# scores words based on chi-squared test to show information gain (http://streamhacker.com/2010/06/16/text-classification-sentiment-analysis-eliminate-low-information-features/)
def create_word_scores():
	# creates lists of all cleitive and gswative words
	cleWords = []
	gswWords = []
	with open(CLE_WIN_FILE, 'r') as cleSentences:
		for i in cleSentences:
			cleWord = re.findall(r"[\w']+|[.,!?;]", i.rstrip())
			cleWords.append(cleWord)
	with open(RT_POLARITY_NEG_FILE, 'r') as gswSentences:
		for i in gswSentences:
			gswWord = re.findall(r"[\w']+|[.,!?;]", i.rstrip())
			gswWords.append(gswWord)
	cleWords = list(itertools.chain(*cleWords))
	gswWords = list(itertools.chain(*gswWords))

	# build frequency distibution of all words and then frequency distributions of words within positive and negative labels
	word_fd = FreqDist()
	cond_word_fd = ConditionalFreqDist()
	for word in cleWords:
		word_fd[word.lower()] += 1
		cond_word_fd['CLE'][word.lower()] += 1
	for word in gswWords:
		word_fd[word.lower()] += 1
		cond_word_fd['GSW'][word.lower()] += 1

	# finds the number of positive and gswative words, as well as the total number of words
	cle_word_count = cond_word_fd['CLE'].N()
	gsw_word_count = cond_word_fd['GSW'].N()
	total_word_count = cle_word_count + gsw_word_count

	# builds dictionary of word scores based on chi-squared test
	word_scores = {}
	for word, freq in word_fd.iteritems():
		cle_score = BigramAssocMeasures.chi_sq(cond_word_fd['CLE'][word], (freq, cle_word_count), total_word_count)
		gsw_score = BigramAssocMeasures.chi_sq(cond_word_fd['GSW'][word], (freq, gsw_word_count), total_word_count)
		word_scores[word] = cle_score + gsw_score

	return word_scores


# finds word scores
word_scores = create_word_scores()


# finds the best 'number' words based on word scores
def find_best_words(word_scores, number):
	best_vals = sorted(word_scores.iteritems(), key=lambda (w, s): s, reverse=True)[:number]
	best_words = set([w for w, s in best_vals])
	return best_words


# creates feature selection mechanism that only uses best words
def best_word_features(words):
	return dict([(word, True) for word in words if word in best_words])


# numbers of features to select
numbers_to_test = [10, 100, 1000, 10000, 15000]
# tries the best_word_features mechanism with each of the numbers_to_test of features
for num in numbers_to_test:
	print 'evaluating best %d word features' % (num)
	best_words = find_best_words(word_scores, num)
	evaluate_features(best_word_features)