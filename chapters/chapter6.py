"""
                       ===> Chapter 6: Reading Documents <===

        --- code samples from the book Web Scraping with Python ---

            The chapter starts talking about how the internet is more than
        just HTML files. Actually, HTML is a rather new format to transfer
        data through the internet.
            Before Html became popular (something around 1992) the internet
        was basically just email sending and file transferring. So, putting
        that way, is easy to see the importance of learning how to read
        documents. although, Html is the main formatting for data on the
        internet today, mainly institutions like governments still use thing
        like PDF files as there main way of sharing information through the
        internet.

"""
from io import StringIO
from urllib.request import urlopen
import csv
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

"""
-----------------------------
Text files 
"""
# for old school sites that share data through text files
# it's rather simple to get the info:
def readText(url='http://www.pythonscraping.com/pages/warandpeace/chapter1-ru.txt'):
    info = urlopen(url)
    return info.read().decode('utf-8')

"""
_____________________________
CSV files
"""

# saving CSV files on the hard disk is bad practice
# so it's better to read it as a string anduse StringIO
# to treat it as a file so we can read as CSV:

def readCSV(url="http://pythonscraping.com/files/MontyPythonAlbums.csv"):
    data = urlopen(url)
    data = data.read().decode()
    dataFile = StringIO(data)
    csvReader = csv.reader(dataFile)
    for row in csvReader:
        print(f"the name of the movie is {row[0]} the year is {row[1]}")

"""
--------------------------
PDF files
"""

def readPDF(pdfFile):
    resourceManager = PDFResourceManager()
    stringFile = StringIO()
    laParams = LAParams()
    device = TextConverter(resourceManager, stringFile, laparams=laParams)

    PDFPage.get_pages(resourceManager, device, pdfFile)
    device.close()

    content = stringFile.getvalue()
    stringFile.close()

    return content

exampleUrl = "http://pythonscraping.com/pages/warandpeace/chapter1.pdf"
pdfFile = urlopen(exampleUrl)
outPut = readPDF(pdfFile)
print(outPut)
pdfFile.close()