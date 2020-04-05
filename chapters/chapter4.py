from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from socket import timeout
from bs4 import BeautifulSoup
import datetime
import random
import json
import time
import re
start = time.time()
random.seed(datetime.datetime.now())


'''
-----------------------------------------------------------------

problem - find the country of the editors of wikipedia pages

My solution is bellow
'''


# if you want this to work get your own access key bruh
def getCountry(ipAddress, accessKey):

    try:

        print("="*60)
        print("inside getCountry()")
        print(f"    making the request....\n    IP:{ipAddress}")
        response = urlopen(
            f"http://api.ipstack.com/{ipAddress}?access_key={accessKey}&format=1", timeout=120).read() \
            .decode('utf-8')
        print("    request was successful!")
        print("exiting getCountry()...")
        print("="*60)

    except HTTPError as e:
        return None
    except timeout:
        print("time exceed :/")
        return None

    responseJson = json.loads(response)

    return responseJson.get("country_name")


# get history pages of Wikipedia articles
def getHistoryPage(articleSoup, completeLink=False):

    try:
        historyPageURL = articleSoup.find("a", text="View history").attrs["href"]
    except AttributeError:
        return None

    if completeLink:
        return "https://en.wikipedia.org" + historyPageURL
    else:
        return historyPageURL


def getEditorsIps(historyURL):

    editorsIPs = []
    try:
        html = urlopen(historyURL)

    except HTTPError as e:
        return editorsIPs

    except AttributeError:
        return editorsIPs

    historySoup = BeautifulSoup(html, features="html.parser")

    for ips in historySoup.findAll("a", {"class": "mw-anonuserlink"}):
        editorsIPs.append(ips.get_text())
    return editorsIPs


editorsIPS = set()
countries = list()
LIMIT = 0


def getEditorsCountries(startingPage, accessKey, limit=None):

    global editorsIPS
    global countries
    global LIMIT

    if limit is not None:
        print(f"LIMIT = {LIMIT}\nexits when: LIMIT > {limit}")
        if LIMIT > limit:
            return "the limit was reached\nexiting function..."

    LIMIT += 1
    wikiUrl = "https://wikipedia.org"

    try:
        html = urlopen(startingPage)
    except HTTPError as e:
        print("http error on the getEditorsCountries()")
        print("error: " + str(e.getcode()))
        return

    except URLError as e:
        print("problem on url: " + startingPage)
        return

    soup = BeautifulSoup(html, features='html.parser')

    for ipAddress in getEditorsIps(getHistoryPage(soup, True)):
        if ipAddress not in editorsIPS:
            country = getCountry(ipAddress, accessKey)
            print(f"IP: {ipAddress} from {country}")
            editorsIPS.add(ipAddress)
            countries.append(country)

    internalLinks = getLinks(startingPage)
    while len(internalLinks):

        nextPage = wikiUrl + internalLinks[random.randint(0, len(internalLinks) - 1)]

        print("="*60)
        print("going to url:" + nextPage)
        getEditorsCountries(nextPage, accessKey, limit)

    return "no internal links\nexiting function..."


def mostFrequent(list_):
    frequent = None
    frequency = 0
    for item in list_:
        currentFrequency = list_.count(item)
        if currentFrequency > frequency:
            frequency = currentFrequency
            frequent = item
    return frequent


'''
-----------------------------------------------------------------

problem - find the country of the editors of wikipedia pages

The solution from the book
'''


def getLinks(articleUrl):
    html = urlopen("http://en.wikipedia.org"+articleUrl)
    bsObj = BeautifulSoup(html)
    return bsObj.find("div", {"id":"bodyContent"}).findAll("a",
    href=re.compile("^(/wiki/)((?!:).)*$"))


def getHistoryIPs(pageUrl):

    # Format of revision history pages is:
    # http://en.wikipedia.org/w/index.php?title=Title_in_URL&action=history
    pageUrl = pageUrl.replace("/wiki/", "")
    historyUrl = "http://en.wikipedia.org/w/index.php?title="\
    +pageUrl+"&action=history"
    print("history url is: "+historyUrl)
    html = urlopen(historyUrl)
    bsObj = BeautifulSoup(html)
    # finds only the links with class "mw-anonuserlink" which has IP addresses
    # instead of usernames
    ipAddresses = bsObj.findAll("a", {"class":"mw-anonuserlink"})
    addressList = set()
    for ipAddress in ipAddresses:
        addressList.add(ipAddress.get_text())
        return addressList

    links = getLinks("/wiki/Python_(programming_language)")
    while len(links) > 0:
        for link in links:
            print("-------------------")
            historyIPs = getHistoryIPs(link.attrs["href"])

        for historyIP in historyIPs:
            print(historyIP)

        newLink = links[random.randint(0, len(links)-1)].attrs["href"]
        links = getLinks(newLink)


if __name__ == "__main__":
    key = "<API_KEY>"
    url = "https://en.wikipedia.org/wiki/Lua_(programming_language)"

    print(getEditorsCountries(url, key, 1000))
    print(f"the country where most of the editors are from is: {mostFrequent(countries)}")

end = time.time()

print("-"*60)
print(f"duration: {end - start}")


# class WikiArticle:
#
#     def __init__(self, startingPage, rLimit=-1):
#
#         random.seed(datetime.datetime.now())
#
#         self.editorsIPS = set()
#         self.countries = list()
#
#         self.rLimit = rLimit
#         self.startingPage = startingPage
#
#
