import linecache
import urllib2
import threading

import sys
from bs4 import BeautifulSoup
import pandas as pd
import pymysql

conn = pymysql.connect(host='localhost', user='root', db='productdata')
conn.set_charset('utf8')
cursor = conn.cursor()
sql = 'SELECT * from `cameras`;'
cursor.execute(sql)
countrow = cursor.execute(sql)
print countrow
price = []
title =[]
link = []
modelNumber = []
idNumber = []
threads = []
images  = []

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)

def findModel(link):
    opener = urllib2.build_opener()
    opener.add_handlers = [('User-agent', 'Mozilla/5.0')]
    page = opener.open(link)
    soup = BeautifulSoup(page)
    correctDiv = soup.find("div", class_="product-details-numbers-wrapper")
    divs = correctDiv.find_all("div")
    found = False
    for div in divs:
        if "Manufacturer" in div.text:
            found = True
            continue
        if found == True:
            return div.text
            found = False
            break

    return "none"

class getPages:
    def getPage(self, pageNumber):
        try:
            opener = urllib2.build_opener()
            opener.add_handlers  = [('User-agent', 'Mozilla/5.0')]
            url = "https://www.thesource.ca/en-ca/computers-and-tablets/ipad-devices-and-tablets/tablets/c/scc-1-1-1?q=%3Arelevance&page=" + str(pageNumber)
            print url
            page = opener.open(url)
            soup = BeautifulSoup(page)
            return soup
        except:
            return None

class scrapingThread (threading.Thread):
    pageNumber = 0
    page_lock = threading.Lock()
    add_lock = threading.Lock()
    gp = getPages()
    def __init__(self):
        super(scrapingThread, self).__init__()
    def run(self):
        while(True):
            with scrapingThread.page_lock:
                soup = getPages.getPage(self.gp,self.pageNumber)
                scrapingThread.pageNumber += 1
                all_div = soup.find_all("div", class_="productListItem")
                if not all_div:
                    break
                else:
                    self.getInformation(soup)
    def getInformation(self,soup):
        print "entered"
        x = 0
        try:
            all_div = soup.find_all("div", class_="productListItem")
            for div in all_div:
                image = div.find("img")
                imageLink = ("http://www.thesource.ca" + image.get("src"))
                print imageLink
                a = div.find("a")
                urlLink = ("http://www.thesource.ca" + a.get("href"))
                name = a.get("title")
                priceDiv = div.find("div", class_="sale-price")
                if not priceDiv:
                    continue
                allSpan = priceDiv.find_all("span")
                priceItem = allSpan[0].text
                modelNumberItem = findModel(urlLink)
                with scrapingThread.add_lock:
                    vendor = "source"
                    print name
                    print urlLink
                    print priceItem
                    print modelNumberItem
                    print imageLink
                    cursor.execute(
                        "INSERT into cameras(Name, Price, Link, ModelNumber, Images, Vendor) VALUES ('%s', '%s', '%s', '%s','%s', '%s')" % \
                        (name, priceItem, urlLink, modelNumberItem, imageLink, vendor))
                    title.append(name)
                    link.append(urlLink)
                    price.append(priceItem)
                    modelNumber.append(modelNumberItem)
                    images.append(imageLink)
                print x
                x = x + 1
        except:
            PrintException()
            return

opener = urllib2.build_opener()
opener.add_handlers  = [('User-agent', 'Mozilla/5.0')]
url = "https://www.thesource.ca/en-ca/cameras-and-camcorders/mirrorless-cameras/bodies/c/scc-5-4-2"
print url
page = opener.open(url)
soup = BeautifulSoup(page)
sc = scrapingThread()
sc.getInformation(soup)

url = "https://www.thesource.ca/en-ca/cameras-and-camcorders/digital-slr-cameras/dslr-bodies/c/scc-5-1-2"
print url
page = opener.open(url)
soup = BeautifulSoup(page)
sc = scrapingThread()
sc.getInformation(soup)

url = "https://www.thesource.ca/en-ca/cameras-and-camcorders/digital-slr-cameras/dslr-bundles/c/scc-5-1-1"
print url
page = opener.open(url)
soup = BeautifulSoup(page)
sc = scrapingThread()
sc.getInformation(soup)

url = "https://www.thesource.ca/en-ca/cameras-and-camcorders/digital-slr-cameras/dslr-lenses-and-flashes/c/scc-5-1-4"
print url
page = opener.open(url)
soup = BeautifulSoup(page)
sc = scrapingThread()
sc.getInformation(soup)

url = "https://www.thesource.ca/en-ca/cameras-and-camcorders/digital-slr-cameras/dslr-lenses-and-flashes/c/scc-5-1-4?q=%3Arelevance&page=1&view=grid"
print url
page = opener.open(url)
soup = BeautifulSoup(page)
sc = scrapingThread()
sc.getInformation(soup)

url = "https://www.thesource.ca/en-ca/cameras-and-camcorders/point-and-shoot-cameras/cameras/c/scc-5-2-1"
print url
page = opener.open(url)
soup = BeautifulSoup(page)
sc = scrapingThread()
sc.getInformation(soup)

url = "https://www.thesource.ca/en-ca/cameras-and-camcorders/point-and-shoot-cameras/cameras/c/scc-5-2-1?q=%3Arelevance&page=1&view=grids"
print url
page = opener.open(url)
soup = BeautifulSoup(page)
sc = scrapingThread()
sc.getInformation(soup)

conn.commit()
conn.close()
df = pd.DataFrame()
df.insert(0, 'ID', range(0, len(title)))
df["Name"] = title
df["Price"] = price
df["Link"] = link
df["ModelNumber"] = modelNumber
df["Images"] = images
df.to_csv("SourceCameras.csv",index=False, encoding='utf-8')
