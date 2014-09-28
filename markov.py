import random

class Choice(object):

	def __init__(self, word, mashNum):
		self.word = word
		self.mashNum = mashNum

class Node(object):

	def __init__(self, key, c, children):
		self.choice = c
		self.children = children
		self.key = key

class Markov(object):
	
	def __init__(self, open_file_1, open_file_2):
		self.cache = {}
		words1 = self.file_to_words(open_file_1)
		words2 = self.file_to_words(open_file_2)
		main_char1 = self.get_main_char(words1)
		main_char2 = self.get_main_char(words2)
		self.database(words1, 0)
		self.database(words2, 1)
		self.word_size = len(words1)
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
				caps.append(word)

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
	def generate_max_transition(self, size=100):
		maxTran = 0
		maxGenWords = []
		for i in range(len(self.words)-2):
			transitions = 0
			gen_words = []
			seed_word = self.words[i], self.words[i+1]
			w1, w2 = seed_word, next_word
			for j in xrange(size):
				for c in self.cache[(w1,w2)]:
'''				