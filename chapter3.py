from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
import time
import datetime
import random
import threading


start = time.clock()
pages = set()


def getLinks(articleLink):

    soup = BeautifulSoup(
        urlopen("https://en.wikipedia.org"),
        features="html.parser")

    soup.find()


if __name__ == "__main__":
    getLinks("")


end = time.clock()

print("=" * 60)

print(f"the program took: {end - start} seconds to execute...")
