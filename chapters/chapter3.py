from urllib.request import urlopen
from urllib.error import URLError
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
import datetime
import random


random.seed(datetime.datetime.now())

allIntLinks = set()
allExtLinks = set()


def getAllExternalLinks(siteUrl):

    # handling request errors
    try:
        html = urlopen(siteUrl)

    except HTTPError as e:
        return e.getcode()
    except URLError:
        return -1

    soup = BeautifulSoup(html, features="html.parser")
    externalLinks = getExternalLinks(soup, splitAddress(siteUrl)[0])
    internalLinks = getInternalLinks(soup, splitAddress(siteUrl)[0])

    for link in externalLinks:
        if link not in allExtLinks:
            allExtLinks.add(link)
            print(f"adding link: {link}")

    for link in internalLinks:
        if link not in allIntLinks:
            allIntLinks.add(link)
            print(f"going to the link: {link}")
            getAllExternalLinks(link)


# Retrieve a list of all internal links in a page
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
                href=re.compile("^(https|www)((?!"+excludeUrl+").)*$")):

        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link.attrs['href'])
    return externalLinks


def splitAddress(address):
    return address.replace("https://", "").split("/")


def getRandomExternalLink(firstPage):
    try:
        html = urlopen(firstPage)
    except HTTPError as e:
        return e.getcode()

    except URLError:
        return -1

    soup = BeautifulSoup(html, features="html.parser")
    externalLinks = getExternalLinks(soup, firstPage)
    if len(externalLinks) == 0:
        internalLinks = getInternalLinks(soup, firstPage)
        if len(internalLinks) <= 1:
            if len(internalLinks) <= 0:
                return 0

            index = 0
        else:
            index = random.randint(0, len(internalLinks) - 1)
        getRandomExternalLink(internalLinks[index])
    else:
        return externalLinks[random.randint(0, len(externalLinks) - 1)]


def followExternalOnly(startingSite):
    externalLink = getRandomExternalLink(startingSite)
    if type(externalLink) is int:
        if externalLink == 0:
            print("the number of link to follow is zero\n"
                  "there is no way to continue the crawl")
            return
        elif externalLink < 0:
            print("the url is unknown")
            return
        else:
            print(f"an error has occur when trying to get the request\n"
                  f"error code: {externalLink}")
            return
    print("Random external link is: " + externalLink)
    print("-"*50)
    followExternalOnly(externalLink)