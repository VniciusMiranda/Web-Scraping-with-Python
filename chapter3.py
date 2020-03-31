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


def getLinks(articleLink):

    soup = BeautifulSoup(
        urlopen("https://en.wikipedia.org" + articleLink),
        features="html.parser")

    try:
        print(soup.body.h1.get_text())
        print(soup.findAll(attrs={"id" : "mw-content-text"}).findAll("p")[0])
        print(soup.find(id="ca-edit").find("span").find("a").attrs['href'])
    except AttributeError as e:
        print("there is something missing in this page")

        for links in soup.findAll("a", {"href": re.compile("^(/wiki/)")}):
            if links.attrs["href"] not in pages:
                newPage = links.attrs['href']
                print("-"*60 + "\n" + newPage)
                pages.add(newPage)
                getLinks(newPage)


if __name__ == "__main__":
    getLinks("")


end = time.clock()

print("=" * 60)

print(f"the program took: {end - start} seconds to execute...")
