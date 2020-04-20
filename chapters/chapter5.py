"""
                   ===> Chapter 5: Storing Data <===

        --- code samples from the book Web Scraping with Python ---

            The chapter started showing the uses of the urllib method,
        urlretrieve(). That part was pretty small and there wasn't much
        new stuff.

            The next topic was a bit more interesting. It was presented
        the csv module in python that helps when storing the data trough
        csv files. basically the only object that was use from this module
        was the writer.

            Started to use a data base to store the data scraped from wiki-
        pedia.There was some setbacks during the installation but it was
        just because I was too careless during the installation process.

            Learned a bit of SQL and about pymySQL. The way that the use of
        the database is abstracted by pymysql is that the whole thing (at
        least for now is how I see the process) is separating the whole
        process in two classes Connection and Cursor. The first is self
        explanatory. Thesecond stores the information about the last query
        made by it self, let's say that a SELECT keyword was use and retrieve
        some rows from the database,this information can be accesses by the
        cursor.

"""

from urllib.request import urlopen, urlretrieve
from urllib.error import HTTPError, URLError
from cryptography.fernet import Fernet
from email.mime.text import MIMEText
import pymysql as sql
import smtplib
import csv
import re
import os
import random
import datetime as dt
from bs4 import BeautifulSoup

"""
++++++++++++++++++++++++
code to get the database password
"""


def getDBPassword(filePath, passwordPath):
    with open(filePath, "rb") as file:
        key = file.read()
    with open(passwordPath, "rb") as file:
        password = file.read()
    return Fernet(key).decrypt(password).decode()



"""
++++++++++++++++++++++++++++
email sending 
"""

def sendEmail(subject, body):
    with smtplib.SMTP_SSL('smtp.gmail.com', port=465) as smtp:
        loginInfo = ["", ""]
        message = MIMEText(body)
        message['To'] = loginInfo[0]
        message['From'] = loginInfo[0]
        message['Subject'] = subject
        smtp.login(loginInfo[0],loginInfo[1])
        smtp.send_message(message)
        smtp.quit()
"""
++++++++++++++++++++++++
SQL Storing code
"""

random.seed(dt.datetime.now())

connection = sql.connect(host='localhost', unix_socket='/var/run/mysqld/mysqld.sock',
                         password=getDBPassword("database/database.key", "database/database.bytes"),
                         user='root',
                         db='mysql',
                         charset='utf8')

cursor = connection.cursor()
cursor.execute("USE wikipedia")


def insertPageIfNotExist(url):
    global cursor
    cursor.execute(f"SELECT * FROM pages WHERE url = %s",(url))
    if cursor.rowcount == 0:
        cursor.execute(f"INSERT INTO pages (url) VALUES (%s)",(url))
        connection.commit()
        return cursor.lastrowid
    else:
        return cursor.fetchone()[0]


def insertLink(fromPageId, toPageId):
    global connection
    global cursor
    cursor.execute("SELECT * FROM links WHERE fromPageId = %s AND toPageId = %s",(int(fromPageId), int(toPageId)))

    if cursor.rowcount == 0:
        cursor.execute(f"INSERT INTO links (fromPageId, toPageId) VALUES (%s, %s)", (int(fromPageId), int(toPageId)))
        connection.commit()


pages = set()
def getSixDegreeLinks(pageUrl, recursionLevel):
    global pages
    if recursionLevel > 4:
        return
    pageId = insertPageIfNotExist(pageUrl)
    print("-"*60)
    print(f"searching for six degree separation pages from:{pageUrl}")

    html = urlopen("http://en.wikipedia.org" + pageUrl)
    soup = BeautifulSoup(html, features="html.parser")
    for link in soup.findAll("a", href=re.compile("^(/wiki/)((?!:).)*$")):

        insertLink(pageId, insertPageIfNotExist(link.attrs["href"]))
        if link not in pages:
            newLink = link.attrs["href"]
            print(f"found new link:{newLink}")
            pages.add(newLink)
            getSixDegreeLinks(pageUrl, recursionLevel + 1)

"""
--------------------------------------------------
"""
def storeToDB(title, content):
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
    print(f"the title text is:{title}")
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
        pass


"""
+++++++++++++++++++++++
Image Downloading code
"""


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

"""
+++++++++++++++++++++
CSV storing code
"""


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


"""
++++++++++++++++++++++++++++++
"""

if __name__ == "__main__":
    sendEmail("TESTING THE BOOT", " Just a test bro.")