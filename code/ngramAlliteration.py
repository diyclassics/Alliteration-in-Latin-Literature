#!/usr/bin/env python
'''
Code used to generate rates of alliteration for APA 2014 study:
"Distant Reading Alliteration in Latin Literature"
Patrick J. Burns, Fordham University

The study evaluates alliteration rates in works of Latin literature
by two related measures: the frequency of alliterative bigrams
(e.g. populumque potentem, Luc. BC 1.2) and the frequency of
semi-alliterative trigrams (e.g. pila minantia pilis, Luc. BC 1.7).
'''

import os
import re
import string
from collections import Counter

processRoot = '../data/process'

#####
#####
##
## Preprocessing scripts
##
#####
#####

def preprocess(source):
	'''
	Desc: Takes formatted document and removes formatting as well as
	removes non-textual information, inc.:
		- Make lowercase
		- Remove punctuation
		- Remove numbers
		- Remove miscellaneous unicode characters
		- Normalize consonantal 'v' to 'u'		
	Input: string
	Output: string
	'''
	processed = source
	processed = processed.lower() # Make lowercase
	processed = processed.translate(None, '!"#$%&\'(),-./:;<=>?@[\\]^_`{|}~') # Remove punctuation, string.punctuation without * and + which are used for section breaks (+) and lacuna (*)
	processed = processed.translate(None, '0123456789') # Remove numbers
	processed = processed.decode("ascii", "ignore").encode("ascii") # Remove miscellaneous unicode characters
	processed = re.sub(r'v',r'u', processed) # Normalizes consonantal 'v' to 'u'
        
	return processed

def remove_vowels(source):
	return source.translate(None, 'aeiou') #Remove vowels

def removeSpaces(source):
	return source.translate(None, ' ') #Remove spaces

def removeNewlines(source):
	return source.translate(None, '\n') #Remove new lines

def wordCount(text):
	'''
	Splits a string into a list using the default and counts the elements.
	Input: string
	Output: integer
	'''
	return len(text.split())

#####
#####
##
## N-Gram tests
##
#####
#####

def getNGrams(text,n):
    '''
    input: string
    output: list of tuples with n elements
    '''
    
    if n < 1:
	return "Error: n must be great than zero."
    if n > wordCount(text):
	return "Error: n must be less than total number of words"
    
    ngrams = []
    
    words = text.split()
    
    for i in range(0,len(words)-n+1):
        ngrams.append(tuple((words[i:i+n])))

    return ngrams

def getAlliterativeBigrams(text):
	'''
	Takes text and generates bigrams; looks at bigrams and keeps only
	the bigrams with the same initial character. Note that because '+'
	and '*' were used elsewhere in the study to keep sections of text
	separate, bigrams with these characters are ignored.
	
	input: string
	output: list of tuples with 2 elements
	'''
	
	excludedCharacters = '+*' # exclude characters used for section breaks or lacuna
    
	bigrams = getNGrams(text,2)
	
	alliterativeBigrams = []
	
	for bigram in bigrams:
	    if bigram[0][0] not in excludedCharacters:
		if bigram[0][0] == bigram[1][0]:
		    alliterativeBigrams.append(bigram)
	
	return alliterativeBigrams

def getSemiAlliterativeTrigrams(text):
	'''
	Takes text and generates bigrams; looks at bigrams and keeps only
	the bigrams with the same initial character. Note that because '+'
	and '*' were used elsewhere in the study to keep sections of text
	separate, bigrams with these characters are ignored.
	
	input: string
	output: list of tuples with 3 elements
	'''
	
	excludedCharacters = '+*' # exclude characters used for section breaks or lacuna
	
	trigrams = getNGrams(text,3)
	
	semiAlliterativeTrigrams = []
	
	for trigram in trigrams:
	    temp = [trigram[0][0],trigram[1][0],trigram[2][0]]
	    
	    if trigram[0][0] == trigram[1][0] or trigram[0][0] == trigram[2][0] or trigram[1][0] == trigram [2][0]:
		semiAlliterativeTrigrams.append(trigram)
	
	for character in excludedCharacters:
	    semiAlliterativeTrigrams = [(a,b,c) for a, b, c in semiAlliterativeTrigrams if a[0] != character and  b[0] != character and c[0] != character]
    
	return semiAlliterativeTrigrams       

#####
#####
##
## Data scripts
##
#####
#####

def alliterationData(filename,text,report=False):
	'''
	Compiles data for analysis using the alliteration scripts
	above. 
	Input:
	    - string containing filename
	    - string containing text
	    - boolean; if True, a summary report is printed to the
	       console; default is False
	Output: string formatted for use in a .csv file for analysis
	'''
	    
	text = preprocess(text)
	    
	words = wordCount(text)
    
	ab = getAlliterativeBigrams(text)
	sat = getSemiAlliterativeTrigrams(text)
	    
	abCount = len(ab)
	satCount = len(sat)
	
	ab1000 = float((abCount*1000)) / words-1
	sat1000 = float((satCount*1000)) / words-2
     
	abCounter = Counter(ab)
	satCounter = Counter(sat)
	result = '%s, %d, %f, %f' % (filename, words, ab1000, sat1000)
	
	if report == True:
	    print "\n-------------------------------"
	    print filename
	    print 'Words: ', words
	    print 'Most frequent alliterative bigrams: ', abCounter.most_common(10)
	    print 'Most frequent semi-alliterative trigrams: ', satCounter.most_common(10)
	    print 'Alliterative Bigrams (#): ', abCount
	    print 'Semi-Alliterative Trigrams (#): ', satCount
	    print 'Alliterative Bigrams (per 1000 words): ', ab1000
	    print 'Semi Alliterative Trigrams (per 1000 words): ', sat1000
	    print "-------------------------------\n"
	
	return result
 
def alliterationDataDirectory(directory):
	'''
	Iterates through directory running the alliteration scripts and
	generating .csv records for analysis.
	Input: string with directory name
	Output: None
	'''
	    
	for root, dirs, filenames in os.walk(directory):
	    for filename in filenames:
		if filename.endswith('.txt'):
		    with open(os.path.join(root, filename),'r') as f:
			text = f.read()
			print alliterationData(filename,text,False)		

if __name__ == '__main__':
    alliterationDataDirectory(processRoot)