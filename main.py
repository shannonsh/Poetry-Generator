import pickle
import random

#################################################################################
#	Haiku generator
#	This program builds a dictionary (programatically referred to as theDict) that  
#	contains a list of words that appear in a sample of writing and the number of 
#	times other words appear after each word, allowing the program to somewhat  
#	emulate the style of the author of the sample. 
#	After being given a first word to use, the program then randomly chooses 
#	another word that occured after the first word in the writing sample, appends
#	the new word to the poem, and continues until it has reached the number of 
#	syllables required for that line. 
#
#	syllable data from: http://www.speech.cs.cmu.edu/cgi-bin/cmudict
#	provided Shakespeare's sonnets sample text from: 
#		http://www.shakespeares-sonnets.com/all.php
#################################################################################

# creates a dictionary of dictionaries containing each word that
# appears in theFile and the number of times other words appear
# after it
# Precondition: theFile is not empty and that the last word of
# theFile appears at least one other time in theFile
#
# @param theFile: the file to be read
# @return successors: a dictionary of dictionaries containing 
#	all the words in theFile as well as the number of times
#	other words appear after each word. 
def wordFrequencies(theFile):
    text_file = open (theFile, "r")
    successors = {}
    previous = 'the'
    for line in text_file:
        words = line.split()
        for word in words:
            word = word.lower()
            if previous in successors:
                entry = successors[previous]
                if word in entry :
                    entry[word] += 1
                else :
                    entry[word] = 1
            else:
                successors[previous] = {word:1}
            previous = word
    return successors


# Takes a theDict and creates a list of words containing each key
# in theDict repeated the number of times listed in the corresponding
# value of the key. For example, generateProbabilityList({'x':2,'y':1})
# will return ['x','x','y'].
# Precondition: the values of theDict are integers.
#
# @param theDict: a dictionary of dictionaries containing 
# the number of times other words appear after each word. 
# @return result: a list of words containing each key in theDict
# duplicated the number of times listed in the corresponding value
# of the key. 
def generateProbabilityList(theDict) : 
	result = []
	theList = theDict.keys()
	for i in theList : 
		for j in range(0, theDict.get(i)) : 
			result = result + [i]
	return result

# loads a database of words with their corresponding number of syllables
f = open("pickled_word_to_syllables.txt","rb")
syllablesDict = pickle.load(f)

# checks if theWord can be inserted into the line without exceeding maxSyllables
#
# @param theWord: the word to be inserted into the line
# @param lineSyllables: the number of syllables in the line before theWord is added
# @param maxSyllables: the maximum number of syllables allowed in the line
# @return syllableCount: the number of syllables in the word. 
#	If syllableCount returns 0, it means that...
# 		- theWord cannot be inserted into the line without the line exceeding 
#		  maxSyllables
# 		- the number of syllables in theWord cannot be determined because it 
#		  is not included in syllablesDict.
def checkSyllables(theWord, lineSyllables, maxSyllables) : 
	syllableCount = 0
	try : 
		syllableCount = syllablesDict.get(theWord)
	#if the dictionary doesn't have an entry for the word
	except Exception as e:
		print(e)
		return 0
	if (syllableCount is None) or (int(syllableCount) + lineSyllables > maxSyllables): 
		return 0
	else : 
		return syllableCount

# Writes a line starting with theWord and with a syllable length of totalSyllables
# using words from theDict
# Preconditions:
# 	- theWord exists in theDict
# 	- theDict is a dictionary of dictionaries containing 
# 	  the number of times other words appear after each word. 
# 	- totalSyllables is positive
# @param theWord: a string that representsthe word that determines what the 
# next words in line will be based on theDict
# @param theDict: a dictionary of dictionaries containing the number of times 
# other words appear after each word. 
# @param totalSyllables: an integer representing the length of the line in 
# syllables
#
# @return line: a string of words appear one after the other according to 
# theDict and whose length in syllables is equal to totalSyllables
# @return False: indicates that there are no words that can fit in line
# without exceeding totalSyllables
def getLine(theWord, theDict, totalSyllables) :
	line = ""
	# syllables represents the current length of line in syllables 
	syllables = 0
	while(syllables < totalSyllables) : 
		# randomly selects a word that was next to theWord in the sample 
		#	text, with a higher probability for words that ppear more 
		#	frequently next to theWord
		nextWordDict = theDict.get(theWord)
		probabilityList = generateProbabilityList(nextWordDict)
		theWord = random.choice(probabilityList).lower()
		# continues picking words that appeared next to theWord in the
		#	sample text until it finds a word that can be added to line
		#	without exceeding totalSyllables
		numSyllables = checkSyllables(theWord, syllables, totalSyllables)
		while (numSyllables == 0 and len(probabilityList) != 0) : 
			theWord = random.choice(probabilityList).lower()
			# removes the word so that it doesn't waste time testing it again
			probabilityList.remove(theWord)
			numSyllables = checkSyllables(theWord, syllables, totalSyllables)
		# if probabilityList is empty, that means all the words that appear
		#	next to theWord cannot fit in line without exceeding totalSyllables
		if(len(probabilityList) == 0) : 
			return False
		line += theWord + " "
		syllables += int(numSyllables)
	return line[0].upper() + line[1:-1]

# repeatedly calls getLine until a valid line is generated. 
# Preconditions:
# 	- theWord exists in theDict
# 	- theDict is a dictionary of dictionaries containing 
# 	  the number of times other words appear after each word. 
# 	- totalSyllables is positive
# @param theWord: a string that representsthe word that determines what the 
# next words in line will be based on theDict
# @param theDict: a dictionary of dictionaries containing the number of times 
# other words appear after each word. 
# @param totalSyllables: an integer representing the length of the line in 
# syllables
# 
# # @return line: a string of words appear one after the other according to 
# theDict and whose length in syllables is equal to totalSyllables
def writeLine(theWord, theDict, numSyllables) : 
	line = getLine(theWord,theDict,numSyllables)
	if line == False : 
		while(line == False) : 
			line = getLine(theWord,theDict,numSyllables)
		return line
	else : 
		return line

# Writes a Haiku (a 3-line poem with a syllable structure of 5-7-5)
#
# @return poem: the complete Haiku
def writeHaiku() : 
	print "Whose style of writing would you like to emulate?"
	print "Give the name of a text file that contains their writing."
	print "If you'd like to use the default file, just press enter."
	goOn = False
	while(goOn == False) :
		theFile = raw_input()
		if theFile == "" : 
			print "Using Shakespeare's sonnets."
			theFile = 'shakespeare.txt'
		try : 
			theDict = wordFrequencies(theFile)
			goOn = True
		except IOError : 
			print "The filename you entered doesn't seem to exist."
			print "Make sure the file is inside the folder 'poem engine' and include the file extension."
			print "Please enter the filename again."
	goOn = False
	print "What word would you like the poem to begin with?"
	while(goOn == False) : 
		firstWord = raw_input().lower()
		if(firstWord in theDict and firstWord in syllablesDict) : 
			goOn = True
		else : 
			print "Please type a more commonly used word or a word that appears in your sample."
	poem = firstWord + ' '
	firstWordSyllables = syllablesDict.get(firstWord)
	# because firstWord is part of the first line of the poem, need to subtract
	# the length of firstWord in syllables from the total syllable length of the
	# line.
	poem += writeLine(firstWord.lower(), theDict, 5 - firstWordSyllables) + '\n'
	poem += writeLine(poem[poem.rfind(' ')+1:-1], theDict, 7) + '\n'
	poem += writeLine(poem[poem.rfind(' ')+1:-1], theDict, 5)
	print "\n" + poem

###################################################################################
#	Freeform poem generator
#	inspired by: http://thinkzone.wlonk.com/PoemGen/PoemGen.htm
#	This program sorts a dictionary of words into different parts of speech, then
#	randomly puts together those words according to preset grammar formats. 
#
#	part of speech data from: http://icon.shef.ac.uk/Moby/mpos.html
#
#	themed concrete nouns from:
#	http://www.writing.com/main/view_item/item_id/1757079-Concrete-Nouns-List
#
#	abstract nouns from:
#	http://examples.yourdictionary.com/examples-of-abstract-nouns.html
###################################################################################

# searches a dictionary of lists to determine whether a value exists in those lists
# Precondition: the values of the dictionary are lists
#
# @param value: the value to be checked
# @param dictionary: the dictionary to be searched
# @return True: value exists within a list in dictionary
# @return False: value does not exist within dictionary
def isInDict(value, dictionary) : 
	for i in dictionary.values() : 
		if value in i : 
			return True
	return False

# reads in a list of sentence patterns from a text file
# Precondition: theFile contains a list of sentence patterns, with one element
# per line and no empty lines throughout the file. 
# Parts of speech is denoted as follows: 
#	[N]		Concrete noun
#	[a]		abstract noun
#	[p]		plural
#	[h] 	noun phrase
#	[V]		verb (usu participle)
#	[t]		verb (intransitive)
#	[i]		verb (intransitive)
#	[A]		Adjective
#	[v]		adverb
#	[C]		conjunction
#	[P]		Preposition
#	[!]		interjection
#	[r]		pronoun
#	[D]		definite article
#	[I]		indefinite article
#	[o]		Nominative
# 
# @param theFile: a string that corresponds to the name of the file that contains
# the list of sentence patterns
# @return sentencePatternList: a list of strings denoting sentence patterns

def readInSentencePattern(theFile) : 
	sentencePatternList = []
	with open(theFile, 'r') as f : 
		for line in f : 
			sentencePatternList += [line]
	return sentencePatternList

# vocab: a dictionary containing all the words and their parts of speech to be used 
#	in the poem
vocab = pickle.load(open('pickled_5000_parts_of_speech.txt','rb'))
# themeDict: a dictionary containing all concrete nouns that correspond to a certain
# theme
themeDict = pickle.load(open('pickled_themeDict.txt','rb'))

# generates a line of freeform poetry according to a theme using the sentencePattern
# Precondition: the parts of speech in sentencePattern are indicated by a set of 
# brackets and one character (ex: [x]) according to the legend defined in the 
# README file
#
# @param sentencePattern: a string that denotes a certain sentence pattern
# @param theme: the theme that the line should be in. 
# @param the line: a string of words that follow the format determined by 
# sentencePattern
def generateLine(sentencePattern, theme) : 
	#contains the index of the first bracket in string
	bracket = sentencePattern.find('[')
	while(bracket >= 0) : 
		#gets the part of speech indicated within brackets (assumes that part of speech
			#is indicated by 1 character)
		partOfSpeech = sentencePattern[bracket+1]
		#candidates is a list of words that are the specific part of speech indicated
			#in sentence
		if(partOfSpeech == 'N') : 
			candidates = themeDict.get(theme)
		else : 
			candidates = vocab.get(partOfSpeech)
		#selects a random candidate
		theWord = candidates[random.randint(0, len(candidates)-1)]
		#inserts the word where the blank part of speech used to be
		sentencePattern = sentencePattern[:bracket] + theWord + sentencePattern[bracket+3:]
		#updates bracket to find the next empty part of speech
		bracket = sentencePattern.find('[')
	return (sentencePattern[0].upper() + sentencePattern[1:]).strip()

# generates a freeform poem by prompting the user for a theme and the length of
# the poem. 
def generatePoem() : 
	print "Please type a theme that is listed below: "
	goOn = False
	while(goOn == False) : 
		themeList = themeDict.keys()
		# copied from http://stackoverflow.com/a/25048690
		for a,b,c in zip(themeList[::3],themeList[1::3],themeList[2::3]):
			print '{:<30}{:<30}{:<}'.format(a,b,c)
		theme = raw_input()
		if theme in themeList : 
			goOn = True
		else : 
			print "Please enter the exact name of a listed theme."
	numLines = int(raw_input("How many lines do you want your poem to be?\n"))
	sentencePatternList = readInSentencePattern('sentencePatterns.txt')
	poem = ""
	#sentencePatternList[random.randint(0,len(sentencePatternList)-1)]
	for i in range(0, numLines) : 
		poem += generateLine(random.choice(sentencePatternList),theme) + "\n"
	print "\n" + poem

# runs this entire program
def main() : 
	print 'What type of poem would you like to generate? Freeform or haiku?'
	goOn = False 
	while(goOn == False) : 
		poemType = raw_input().lower()
		if(poemType == 'haiku') : 
			goOn = True
			writeHaiku()
		elif(poemType == 'freeform') : 
			goOn = True
			generatePoem()
		else : 
			print "Please enter either 'haiku' or 'freeform'"

main()
