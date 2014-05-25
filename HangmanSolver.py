import re, glob, os
class HangmanSolver:
	def __init__(self):
		self.correct = set()
		self.incorrect = set()
		
		# build dictionarys
		self.two = self.two_letter()
		self.word_lengths = self.build_lengths()
		self.word_frequency = self.build_freq()

	# build dictionary. Maps lengths to a list of words with that length
	def build_lengths(self):
		duplicates = set()
		length_freq = {}
		for file in glob.glob("words/SCOWL/*.*"):
			words = open(file, "r")
			for word in words.readlines():
				word = word.strip().lower()
				if word not in duplicates:
					if len(word) in length_freq:
						length_freq[len(word)].append(word)
					else:
						length_freq[len(word)] = [word]
					duplicates.add(word)
		return length_freq

	# build dictionary of word and it's corresponding frequency 
	def build_freq(self):
		word_freq = {}
		words = open("words/word_frequency.txt","r")
		for word in words.readlines():
			info = word.split("\t")
			if info[0] in word_freq:
				word_freq[info[0]] += int(info[3].strip())
			else:
				word_freq[info[0]] = int(info[3].strip())

		return word_freq

	# returns list of common two letter words
	def two_letter(self):
		two_array = []
		words = open("words/2letter.txt", "r")
		for word in words.readlines():
			word = word.strip().lower()
			two_array.append(word)
		return two_array

	# go through all the candidate words and returns the frequency list of 
	# characters based on the words
	def freq_list(self,words):
		freq_list = {}
		for word in words:
			for char in word:
				if char in freq_list:
					freq_list[char] += 1
				else:
					freq_list[char] = 1
		# delete the alreay guessed characters
		for guess in self.correct:
			freq_list.pop(guess, None)
		return freq_list

	# return max character based on frequency list
	def character(self,freq):
		frequency = 0
		char = 'a'
		for k,v in freq.iteritems():
			if v > frequency:
				char = k
				frequency = v
		return char

	# returns character based on a frequency analysis of the most popular words
	# finds the most popular word and then compares that word to the current word to 
	# see what characters are missing
	def freq_analysis(self, words, guessing):
		best_word = None
		frequency = 0
		for word in words:
			if word in self.word_frequency and self.word_frequency[word] > frequency:
				frequency = self.word_frequency[word]
				best_word = word

		# compare the best word to the current word we're guessing to find where they 
		# aren't the same
		for i in range(0, len(best_word)):
			if best_word[i] != guessing[i]:
				return best_word[i]

		# this would be an error since the guessing word has no _'s in it
		return None


	#create possible words from a regex and all words
	def possible_words(self,regex, words):
		output = []
		for word in words:
			match = re.match(regex, word)
			if match:
				output.append(word)
		return output

	# guess randomly by chossing a character that hasn't been guessed yet
	def guess_randomly(self):
		for letter in range(ord('a'), ord('z') + 1):
					cur_letter = str(chr(letter)) 
					if cur_letter not in self.correct and cur_letter not in self.incorrect:
						return cur_letter
		return None

	# takes in a state and returns character
	def make_guess(self,state):

		# find the word that has the least amount of _'s in it
		guessing = None
		blanks = 100
		for word in state.split(" "):
			if (word.count("_") < blanks and word.count("_") > 0):
				blanks = word.count("_")
				guessing = word

		# special cases for one letter words--likely either a or i
		if len(guessing) == 1:
			if "a" not in self.correct and "a" not in self.incorrect:
				return "a"
			elif "i" not in self.correct and "i" not in self.incorrect:
				return "i"
			else:
				# go through and return the first character that isn't correct or incorrect
				return self.guess_randomly()

		# set words to all possible words with guessing's length
		if len(guessing) in self.word_lengths:
			words = self.word_lengths[len(guessing)]
		else:
			return self.guess_randomly()

		# special case for words of length 2
		if len(guessing) == 2:
			words = self.two

		regex= guessing.replace("_", "[^%s]" % "".join(list(self.incorrect) + list(self.correct)) if (self.incorrect or self.correct) else "[a-z]")
		matches = self.possible_words(regex, words)

		# if matches is less than 30 do a analysis based on how popular each word is, choose the word that is the most popular
		if len(matches) < 100 and len(guessing) != 2 and len(matches) > 1:
			return self.freq_analysis(matches, guessing)

		if not matches:
			return self.guess_randomly()

		guess = self.character(self.freq_list(matches))
		return guess