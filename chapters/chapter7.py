"""
             ===> Chapter 7: Cleaning Your Dirty Data <===

        --- code samples from the book Web Scraping with Python ---

            This chapter title is pretty descriptive. The web is a place
        where is easy to get thing that you didn't expect, that's why is
        important to write defensive code to handle this bad formatted data
        as if you were handling errors.

            In linguistic exist the concept of n-grams that is basically a
        sequence of words that are usually use in text and the chapter starts
        by defining the concept of n-gram and giving a sample code to get n-grams,
        in this case it is a 2-gram formatter.
            
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError
import re
import string

def n_grams(input, n):
    '''
    :param input: text
    :param n: number of words
    :return: all n-grams of the text
    '''
    output = list()
    for i in range(len(input) + n - 1):
        output.append(input[i: i + n])

    return output


def clean_input(input):
    input = re.sub("\n+", " ", input)
    input = re.sub(" +", " ", input)
    input = re.sub("\[[0-9]*\]", "", input)
    input = bytes(input, "UTF-8")
    input = input.decode("ascii", "ignore")

    cleanInput = list()
    print(type(input))
    input = input.split(' ')
    for item in input:
        item = item.strip(string.punctuation)
        if len(item) > 1 or (item.lower() == 'a' or item.lower() == 'i'):
            cleanInput.append(item)

    return cleanInput
if __name__ == "__main__":
    try:
        html = urlopen("http://en.wikipedia.org/wiki/Python_(programming_language)")
    except HTTPError as error:
        print(error.getcode())

    soup = BeautifulSoup(html, features="html.parser")
    content = soup.find("div", {"id": "mw-content-text"}).get_text()
    content = clean_input(content)
    ngrams = n_grams(content, 2)
    print(ngrams)
    print("number of n grams of 2 is: {0}".format(len(ngrams)))
