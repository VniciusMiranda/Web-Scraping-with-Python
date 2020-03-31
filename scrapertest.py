from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
import time
import datetime
import random
import threading


_FINISH = False

random.seed(datetime.datetime.now())

start = time.clock()


def checkQuit():
    global _FINISH

    while not _FINISH:
        ip = input()
        if ip == "q":
            _FINISH = True


def getLinks(articleLink):
    try:
        html = urlopen("https://en.wikipedia.org/" + articleLink)
    except HTTPError as e:
        print(e)
        return None

    try:
        soup = BeautifulSoup(html, features="html.parser")
    except AttributeError as e:
        print(e)
        return None

    return soup.find("div", {"id": "bodyContent"}).findAll("a", {"href": re.compile("^(/wiki/)((?!:).)*$")})


exitThread = threading.Thread(name="exitThread", target=checkQuit)
exitThread.start()

if __name__ == "__main__":

    links = getLinks("/wiki/Library_Genesis")

    while not _FINISH:
        if not len(links) > 0:
            break
        print(f"len(links) = {len(links)}")
        newArticle = links[random.randint(0, len(links) - 1)].attrs["href"]
        print(newArticle)
        links = getLinks(newArticle)


end = time.clock()

print("=" * 60)

print(f"the program took: {end - start} seconds to execute...")
