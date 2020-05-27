"""
             ===> Chapter 8: Reading and Writing Natural Languages <===

             --- code samples from the book Web Scraping with Python ---

                This chapter introduces the idea of natural language analysis
            and uses as an example of it the google algorithm.

"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import string
import operator
import pprint
from random import randint


def wordListSum(wordList):
    sum = 0
    for word, value in wordList.items():
        sum += value
    return sum


def retrieveRandomWord(wordList):
    randIndex = randint(1, wordListSum(wordList))
    for word, value in wordList.items():
        randIndex -= value
        if randIndex <= 0:
            return word


def buildWordDict(text):
    # remove new lines and quotes
    text = text.replace("\n"," ")
    text = text.replace('"', "")

    # make sure punctuation marks are treated as their own "words",
    #so that they will be included in the markov chain
    punctuation = [',', '.', ';', ':']
    for symbol in punctuation:
        text = text.replace(symbol, " " + symbol + " ")

    words = text.split(" ")
    # filter out empty words
    words = [word for word in words if word != ""]

    wordDict = {}
    for i in range(1, len(words)):
        if words[i - 1] not in wordDict:
            # create a new dictionary for this word
            wordDict[words[i - 1]] = {}
        if words[i] not in wordDict[i - 1]:
            wordDict[words[i - 1]][words[i]] = 0


# ----------------------------  getting the most common words  -----------------------------


def isCommon(ngram):
    commonWords = ["the", "be", "and", "of", "a", "in", "to", "have", "it",
    "i", "that", "for", "you", "he", "with", "on", "do", "say", "this",
    "they", "is", "an", "at", "but","we", "his", "from", "that", "not",
    "by", "she", "or", "as", "what", "go", "their","can", "who", "get",
    "if", "would", "her", "all", "my", "make", "about", "know", "will",
    "as", "up", "one", "time", "has", "been", "there", "year", "so",
    "think", "when", "which", "them", "some", "me", "people", "take",
    "out", "into", "just", "see", "him", "your", "come", "could", "now",
    "than", "like", "other", "how", "then", "its", "our", "two", "more",
    "these", "want", "way", "look", "first", "also", "new", "because",
    "day", "more", "use", "no", "man", "find", "here", "thing", "give",
    "many", "well"]
    for word in ngram:
        if word in commonWords:
            return True
    return False


# basically the function from chap 7 with some tweaks
def clean_input(input):
    input = re.sub('\n'," ", input)
    input = re.sub('\[[0-9]*\]', " ", input)
    input = re.sub(' +', " ", input)
    input = bytes(input, "UTF-8")
    input = input.decode("ascii", "ignore")

    cleanInput = []
    input = input.split(" ")
    for item in input:
        item = item.strip(string.punctuation)
        if (len(item) > 1 or (item.lower() == 'a' or item.lower() == 'i')):
            cleanInput.append(item)

    return cleanInput


def n_grams(input, n):
    input = clean_input(input)

    output = {}
    for i in range(len(input) - (n + 1)):

        if not isCommon(input[i:i+n]):
            ngramTemp = " ".join(input[i:i+n])

            if ngramTemp not in output:
                output[ngramTemp] = 0
            output[ngramTemp] += 1

    return output


if __name__ == "__main__":
    content = str(
        urlopen("http://pythonscraping.com/files/inaugurationSpeech.txt").read(),
        'utf-8'
    )
    nGrams = n_grams(content, 2)
    sortedNGrams = sorted(nGrams.items(), key= operator.itemgetter(1), reverse=True)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(sortedNGrams)
