"""
                   ===> Chapter 5: Storing Data <===

        --- code samples from the book Web Scraping with Python ---



"""

from urllib.request import urlretrieve
from urllib.request import urlopen
import os

from bs4 import BeautifulSoup

downloadDirectory = "downloaded"
baseUrl = "http://pythonscraping.com"


# just trying a new style, with more typing
def getAbsoluteURL(baseUrl : str, source: str) -> str or None:
    if source.startswith("http://www"):
        url = "http://" + source[11:]
    elif source.startswith("http://"):
        url = source
    elif source.startswith("www."):
        url = source[4:]
        url = "http://" + source

    else:
        url = baseUrl + "/" + source
    if baseUrl not in url:
        return None

    return url


html = urlopen(baseUrl)
soup = BeautifulSoup(html, features="html.parser")
downloadList = soup.findAll()

for download in downloadList:
    print(download)
    fileUrl = getAbsoluteURL(baseUrl, download.attrs["src"])
    if fileUrl is not None:
        print(fileUrl)

