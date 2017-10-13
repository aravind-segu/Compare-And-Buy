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
sql = 'SELECT * from `television`;'
cursor.execute(sql)
countrow = cursor.execute(sql)
print(countrow)
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
            url = "https://www.thesource.ca/en-ca/tvs-and-home-theatre/televisions/led-tvs/c/scc-7-1-1?q=%3Arelevance&page=" + str(pageNumber) + "&view=grid"
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
                    mapping = 1
                    cursor.execute(
                        "INSERT into television(Name, Price, Link, ModelNumber, Images, Vendor, tvMapping) VALUES ('%s', '%s', '%s', '%s','%s', '%s', %d)" % \
                        (name, priceItem, urlLink, modelNumberItem, imageLink, vendor, mapping))
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

thread1 = scrapingThread()
thread2 = scrapingThread()
thread3 = scrapingThread()
thread4 = scrapingThread()

thread1.start()
thread2.start()
thread3.start()
thread4.start()

thread1.join()
thread2.join()
thread3.join()
thread4.join()

st = scrapingThread()

opener = urllib2.build_opener()
opener.add_handlers = [('User-agent', 'Mozilla/5.0')]
url = "https://www.thesource.ca/en-ca/tvs-and-home-theatre/televisions/4k-tvs/c/scc-7-1-3?q=%3Arelevance&page=0&view=grid"
page = opener.open(url)
soup = BeautifulSoup(page)
scrapingThread.getInformation(st, soup)

opener = urllib2.build_opener()
opener.add_handlers = [('User-agent', 'Mozilla/5.0')]
url = "https://www.thesource.ca/en-ca/tvs-and-home-theatre/televisions/4k-tvs/c/scc-7-1-3?q=%3Arelevance&page=1&view=grid"
page = opener.open(url)
soup = BeautifulSoup(page)
scrapingThread.getInformation(st, soup)

conn.commit()
conn.close()
df = pd.DataFrame()
df.insert(0, 'ID', range(0, len(title)))
df["Name"] = title
df["Price"] = price
df["Link"] = link
df["ModelNumber"] = modelNumber
df["Images"] = images

df.to_csv("SourceTVs.csv",index=False, encoding='utf-8')
