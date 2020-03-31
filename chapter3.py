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


# Retrive a list of all internal links in a page
def getInternalLinks(soup, includeUrl):
    internalLinks = []

    # Finds all links that begin with a "/"
    for link in soup.findAll("a", href=re.compile("^(/|.*"+includeUrl+")")):

        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                internalLinks.append(link.attrs['href'])
    return internalLinks


# Retrieves a list of all external links found on a page
def getExternalLinks(soup, excludeUrl):
    externalLinks = []

    # Finds all links that start with "http" or "www" that do
    # not contain the current URL
    for link in soup.findAll("a",
                href=re.compile("^(http|www)((?!"+excludeUrl+").)*$")):

        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link.attrs['href'])
    return externalLinks


if __name__ == "__main__":
    pass


end = time.clock()

print("=" * 60)

print(f"the program took: {end - start} seconds to execute...")
