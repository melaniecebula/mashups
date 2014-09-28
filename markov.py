import random
import enchant
import operator
import nltk

d = enchant.Dict("en_US")
word_counts = {}
class Choice(object):

	def __init__(self, word, mashNum):
		self.word = word
		self.mashNum = mashNum

class Markov(object):
	
	def __init__(self, open_file_1, open_file_2):
		self.cache = {}
		words1 = self.file_to_words(open_file_1)
		words2 = self.file_to_words(open_file_2)
                main_name1 = self.get_main_name(words1)
                main_name2 = self.get_main_name(words2)
                words2 = self.replace_words(main_name1, main_name2, words2)
		self.database(words1, 0)
		self.database(words2, 1)
		self.word_size = len(words1)
		self.words = words1 + words2
		
        def replace_words(self, main_name1, main_name2, words):
            for i in range(len(words)):
                if words[i] == main_name2:
                    print words[i]
                    words[i] = main_name1
                    print words[i]
            return words

	def file_to_words(self, open_file):
		open_file.seek(0)
		data = open_file.read()
		words = data.split()
		return words
		
        def name_features(self, word):
            count = 0
            if word in word_counts:
                count = word_counts[word]
            return {'upper_case': word[0].isupper(), 'in_dict': not d.check(word.lower()), 'num_times': count}

        def get_main_name(self, words):
            self.get_word_counts(words)
            results = self.get_training_data(words)
            random.shuffle(results)
            featuresets = [(self.name_features(n), name) for (n, name) in results]
            length = len(featuresets)
            train_set, test_set = featuresets[length/2:], featuresets[:length/2]
            classifier = nltk.NaiveBayesClassifier.train(train_set)
            result = [(word, classifier.classify(self.name_features(word))) for word in words]
            res = []
            for pair in result:
                word, is_name = pair
                if is_name == "name":
                    res.append(word)
            final_word_counts = {}
            for word in res:
                if word not in final_word_counts:
                    final_word_counts[word] = 1
                else:
                    final_word_counts[word] += 1
            return max(final_word_counts.iteritems(), key=operator.itemgetter(1))[0]

        def get_training_data(self, words):
            results = []
            for word in words:
                word = word.decode('string_escape')
                word = word.replace(",", "")
                word = word.replace(".", "")
                word = word.replace("!", "")
                if word[0].isupper() and not d.check(word.lower()):
                    results.append((word, "name"))
                else:
                    results.append((word, "not-name"))
            return results

        def get_word_counts(self, words):
		caps = []
		for word in words:
			if word[0].isupper():
                                word = word.decode('string_escape')
                                word = word.replace(",", "")
                                word = word.replace(".", "")
                                word = word.replace("!", "")
				caps.append(word)
                for cap in caps:
                    temp = cap.lower()
                    if d.check(temp) or d.check(cap):
                        caps.remove(cap)
                for cap in caps:
                    if cap in word_counts:
                        word_counts[cap] += 1
                    else:
                        word_counts[cap] = 1

	def get_main_char(self, words):
                loc_word_counts = {}
		caps = []
		for word in words:
			if word[0].isupper():
                                word = word.decode('string_escape')
                                word = word.replace(",", "")
                                word = word.replace(".", "")
                                word = word.replace("!", "")
				caps.append(word)
                for cap in caps:
                    temp = cap.lower()
                    if d.check(temp) or d.check(cap):
                        caps.remove(cap)
                for cap in caps:
                    if cap in loc_word_counts:
                        loc_word_counts[cap] += 1
                    else:
                        loc_word_counts[cap] = 1

                return max(loc_word_counts.iteritems(), key=operator.itemgetter(1))[0]

	def triples(self, words):
		if len(words) < 3:
			return
		for i in range(len(words) - 2):
			yield (words[i], words[i+1], words[i+2])
                yield words[-2], words[-1], words[0]
                yield words[-1], words[0], words[1]
			
	def database(self, words, mashNum):
		for w1, w2, w3 in self.triples(words):
			key = (w1, w2)
			if key in self.cache:
				self.cache[key].append(Choice(w3, mashNum))
			else:
				self.cache[key] = [Choice(w3, mashNum)]

	def choose(self, w1, w2, mashNum):
		choices = self.cache[(w1,w2)]
		transitions = []
		notTransitions = []
		for choice in choices:
			if choice.mashNum != mashNum:
				transitions.append(choice.word)
			else:
				notTransitions.append(choice.word)
		if len(transitions):
			return (w2, random.choice(transitions), int(not mashNum))
		else:
			return (w2, random.choice(notTransitions), int(mashNum))

        def generate_markov_text(self, size=25):
                maxtransitions = 0
                g_w = []
                for i in range(5):
                        transitions = 0
                        seed = random.randint(0, self.word_size-3)
                        seed_word, next_word = self.words[seed], self.words[seed+1]
                        w1, w2 = seed_word, next_word
                        gen_words = []
                        mashNum = 0
                        for i in xrange(size):
                                gen_words.append(w1)
                                w1, w2, t = self.choose(w1,w2,mashNum)
                                if (not t == mashNum):
                                        transitions = transitions + 1
                                        mashNum = t
                        gen_words.append(w2)
                        if transitions > maxtransitions:
                                maxtransitions = transitions
                                g_w = gen_words
                return ' '.join(g_w)
'''
	def generate_like_text(self, text):
		seed = random.randint(0, len(text) - 3)
		seed_word, next_word = text[seed], text[seed+1]
'''
