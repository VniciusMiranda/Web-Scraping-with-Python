"""
                   ===> Chapter 5: Storing Data <===

        --- code samples from the book Web Scraping with Python ---

            The chapter started showing the uses of the urllib method,
        urlretrieve(). The part of the code bellow where an example is
        given was partially made by me by just modifying the code example
        from the book that was getting some links of js files, when the
        initial objective was to download only the images of the site.
            Started to use a data base to store the data scraped from wiki-
        pedia. There was some setbacks during the installation but it was
        mostly small stuff. Learned a bit of SQL and about pymySQL. The way
        that the use of the data base is abstracted by pymysql is that the
        whole thing (at least for now is how I see the process) is separated
        in two classes Connection and Cursor. An instance of the Connection
        class is responsible for handling the data that is sent to the data
        base, handling rollbacks and creating Cursors. A cursor keeps track of
        certain state information, such as which database it is using. If you
        have multiple databases and need to write information across all of them,
        you might have multiple cursors to handle this. A cursor also contains the
        results of the latest query it has executed. By calling functions on the cursor,
        such as cur.fetchone() , you can access this information.


"""

from urllib.request import urlopen, urlretrieve
from urllib.error import HTTPError, URLError
import csv
import pymysql as sql
import re
import os
import random
import datetime as dt
from bs4 import BeautifulSoup


random.seed(dt.datetime.now())

connection = sql.connect(host='localhost', unix_socket='/var/run/mysqld/mysqld.sock',
                         password='Piloto_052399651', user='root', db='mysql', charset='utf8')

cursor = connection.cursor()
cursor.execute("USE scraping")

downloadDirectory = "downloaded"
baseURL = "http://pythonscraping.com"


def storeToDB(title, content: str):
    global cursor

    title = title.replace('"', "")
    content = content.replace('"', "")
    print(f'executing query INSERT INTO pages (title, content ) VALUES ("{title}", "{content}")')
    cursor.execute(f'INSERT INTO pages (title, content ) VALUES ("{title}", "{content}")')
    cursor.connection.commit()
    print("committed successfully")


def getLinks(articleLink):
    try:
        html = urlopen("https://en.wikipedia.org" + articleLink)
    except HTTPError as e:
        print(f"HTTP error\ncode: {e.getcode()}\n returning None")
        return None
    except URLError:
        print("url error\nreturning None...")
        return None

    soup = BeautifulSoup(html, features="html.parser")

    title = soup.find("h1").get_text()
    print(f"the title text is:{title }")
    content = soup.find("div", {"id": "mw-content-text"}).find("p", attrs=None).get_text()
    print(f"the title text is:{content}")
    storeToDB(title, content)
    print("retrieving links...")
    links = soup.find("div", {"id": "bodyContent"}).findAll("a", href=re.compile("^(/wiki/)((?!:).)*$"))
    print("successfully retrieved the links")
    return links


def getWiki(limit=None):
    global cursor
    global connection
    counter = 0
    links = getLinks("/wiki/Kevin_Bacon")

    try:
        while len(links) > 0:
            if limit is not None:
                if counter > limit:
                    break
            newArticle = links[random.randint(0, len(links) - 1)].attrs["href"]
            print(f"going to {newArticle}")
            print("-"*60)
            links = getLinks(newArticle)
    finally:

        cursor.close()
        connection.close()


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


if __name__ == "__main__":
    getWiki(100)


