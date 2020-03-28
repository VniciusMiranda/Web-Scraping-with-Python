from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup


def get_title(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        print(e)
        return None

    try:
        soup = BeautifulSoup(html.read(), features="html.parser")
        title = soup.body
    except AttributeError as e:
        return None

    return title


if __name__ == "__main__":

    url = "http://www.pythonscraping.com/pages/page3.html"

    title = get_title(url)

    if title is None:
        print("title could not be found")

    else:

        print(title.get_text())
