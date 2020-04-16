"""
                   ===> Chapter 5: Storing Data <===

        --- code samples from the book Web Scraping with Python ---

            The chapter started showing the uses of the urllib method,
        urlretrieve(). The part of the code bellow where an example is
        given was partially made by me by just modifying the code example
        from the book that was getting some links of js files, when the
        initial objective was to download only the images of the site.


"""

from urllib.request import urlopen, urlretrieve
from urllib.error import HTTPError, URLError
import csv
import pymysql as sql
import os

from bs4 import BeautifulSoup

"""
the example of the book happens to be pretty inconsistent
so I decided to create my own example for this.
the code bellow is all mine heheheheh
"""
downloadDirectory = "downloaded"
baseURL = "http://pythonscraping.com"


def getImages(url: str) -> int or list:
    """
    :param url: str
    :return:{
        if ERROR is not None:
            return int
        else:
            return list
    }
    """
    try:
        html = urlopen(url)
    except HTTPError as e:
        print(f"http error\ncode:{e.getcode()}")
        return e.getcode()
    except URLError as e:
        print(f"URL error")
        return 0

    soup = BeautifulSoup(html, features="html.parser")

    urls = list()
    for img in soup.findAll(src=True):
        imgUrl = img["src"]
        if url in imgUrl and (imgUrl.find(".jpg") or imgUrl.find(".png")) is not -1:
            urls.append(imgUrl)

    return urls


def getDownloadPath(baseUrl: str, downloadUrl: str, downloadDir: str) -> str:
    path = downloadUrl.replace("www.", "").replace(baseUrl, "")
    path = downloadDir + path
    directory = os.path.dirname(path)
    print("="*50)
    print("inside get download path function")
    print(f"the directory is {directory}")
    exists = os.path.exists(directory)

    if not exists:
      os.makedirs(directory)

    return path


def test_csv():
    with open("../files/test.ods", "w+") as test:
        writer = csv.writer(test)
        head = ["number", "number plus 2", "number 2 times"]
        writer.writerow(head)
        for i in range(10):
            row = [i, i + 2, i * 2]
            writer.writerow(row)


def wikiTableToCSV(url: str, csvPath):
    try:
        html = urlopen(url)
    except HTTPError as e:

        print(f"HTTP error:\ncode: {e.getcode()}")
        return e.getcode()
    except URLError:
        print("error on the URL\nreturning None...")
        return None

    soup = BeautifulSoup(html, features="html.parser")
    rows = soup.find("table", {"class": "wikitable"}).findAll("tr")

    with open(csvPath, "w+") as file:
        writer = csv.writer(file)

        for row in rows:
            csvRow = []
            for cell in row.findAll(["td", "th"]):
                text = cell.get_text().replace("\n", "")

                csvRow.append(text)

            writer.writerow(csvRow)


def dataBase():
    connection = sql.connect(host='127.0.0.1', unix_socket='/var/run/mysqld/mysqld.sock',
                             user='root', passwd='Piloto_052399651', db='mysql')

    cursor = connection.cursor()


if __name__ == "__main__":

    wikiTableToCSV("https://en.wikipedia.org/wiki/Comparison_of_text_editors", "../files/test.csv")



