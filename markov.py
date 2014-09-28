import random
import enchant
import operator

class Choice(object):

	def __init__(self, word, mashNum):
		self.word = word
		self.mashNum = mashNum

class Markov(object):
	
	def __init__(self, open_file_1, open_file_2):
		self.cache = {}
		words1 = self.file_to_words(open_file_1)
		words2 = self.file_to_words(open_file_2)
		main_char1 = self.get_main_char(words1)
		main_char2 = self.get_main_char(words2)
		self.database(words1, 0)
		self.database(words2, 1)
		self.word_size = len(words1) + len(words2)
		self.words = words1 + words2
		
	def file_to_words(self, open_file):
		open_file.seek(0)
		data = open_file.read()
		words = data.split()
		return words
		
	def get_main_char(self, words):
		caps = []
		for word in words:
			if word[0].isupper():
                                word = word.decode('string_escape')
                                word = word.replace(",", "")
                                word = word.replace(".", "")
                                word = word.replace("!", "")
				caps.append(word)
                d = enchant.Dict("en_US")
                for cap in caps:
                    temp = cap.lower()
                    if d.check(temp) or d.check(cap):
                        caps.remove(cap)
                word_counts = {}
                for cap in caps:
                    if cap in word_counts:
                        word_counts[cap] += 1
                    else:
                        word_counts[cap] = 1
                return max(word_counts.iteritems(), key=operator.itemgetter(1))[0]

	def triples(self, words):
		if len(words) < 3:
			return
		for i in range(len(words) - 2):
			yield (words[i], words[i+1], words[i+2])
			
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
		seed = random.randint(0, self.word_size-3)
		seed_word, next_word = self.words[seed], self.words[seed+1]
		w1, w2 = seed_word, next_word
		gen_words = []
		mashNum = 0
		for i in xrange(size):
			gen_words.append(w1)
			w1, w2, mashnum = self.choose(w1,w2,mashNum)
		gen_words.append(w2)
		return ' '.join(gen_words)
'''
	def generate_like_text(self, text):
		seed = random.randint(0, len(text) - 3)
		seed_word, next_word = text[seed], text[seed+1]
'''
