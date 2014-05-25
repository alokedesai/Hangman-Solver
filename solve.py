import argparse, re
from HangmanSolver import HangmanSolver

# parser to determine the word and the number of guesses 
parser = argparse.ArgumentParser(description='A Hangman Solver')
parser.add_argument('-g','--guess', help='The number of guesses', required=True)
parser.add_argument('-w','--word', help='The word or phrase to be solved', required=True)
args = vars(parser.parse_args())

WORD = args["word"].lower().strip()
cur_word = re.sub("[a-z]", "_", WORD)
num_guesses = args["guess"]


#Hangman Runner that actually solves the phrase or word
solver = HangmanSolver()
guesses =0

# finds if a chracter is in the candidate word, if so, update the cur_word
def find(str, ch):
	for i, ltr in enumerate(str):
		if ltr == ch:
			global cur_word
			cur_word = cur_word[0:i] + ltr + cur_word[i+1:len(cur_word)]
			yield i

# simple guess function that returns boolean whether char is in WORD
def guess(char):
	return list(find(WORD,char))

while (cur_word != WORD and guesses <= int(num_guesses)):
	char = solver.make_guess(cur_word)
	if guess(char):
		solver.correct.add(char)
	else:
		solver.incorrect.add(char)
		guesses +=1
	print "guessed: %s and the word currently is: %s" % (char, cur_word)
	
# hangman was solved
if cur_word == WORD:
	print "Hangman Solver solved the word with %d incorrect guesses!" % guesses
else:
	print "Hangman Solver was unable to solve the word in %s guesses. The solver got to '%s' when it ran out of guesses." % (num_guesses,cur_word)
