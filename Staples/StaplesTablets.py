import linecache
import urllib2
import threading
from bs4 import BeautifulSoup
import pandas as pd
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
price = []
title = []
link = []
modelNumber = []
idNumber = []
images = []
threads = []

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)

class getPages:
    def getPage(self, pageNumber):
        try:
            opener = urllib2.build_opener()
            opener.add_handlers = [('User-agent', 'Mozilla/5.0')]
            url = "https://www.staples.ca/en/Tablets/cat_CL200622_2-CA_1_20001?fids=&pn=" + str(pageNumber) + "&sr=true&sby=&min=&max="
            print url
            page = opener.open(url)
            soup = BeautifulSoup(page)
            return soup
        except:
            return None

class scrapingThread (threading.Thread):
    pageNumber = 1
    pageLock = threading.Lock()
    addLock = threading.Lock()
    gp = getPages()
    def __init__(self):
        super(scrapingThread, self).__init__()
    def run(self):
        # while(scrapingThread.pageNumber <= 3):
        #     with scrapingThread.pageLock:
        #         print scrapingThread.pageNumber
        #         soup = getPages.getPage(self.gp, self.pageNumber)
        #         scrapingThread.pageNumber += 1
        #         all_div = soup.findAll("div", {"typeof":"Product"})
        #         print all_div
        #         if not all_div:
        #             break
        #         else:
        opener = urllib2.build_opener()
        opener.add_handlers = [('User-agent', 'Mozilla/5.0')]
        url1 = "https://www.staples.ca/en/Tablets/cat_CL200622_2-CA_1_20001"
        print url1
        page1 = opener.open(url1)
        soup1 = BeautifulSoup(page1)
        self.getInformation(soup1)
        soup2 = BeautifulSoup(open("./staplesTablets2.html"))
        self.getInformation(soup2)
        soup3 = BeautifulSoup(open("./staplesTablets3.html"))
        self.getInformation((soup3))
    def getInformation(self, soup):
        x = 0
        try:
            all_divs = soup.findAll("div", {"typeof":"Product"})
            for div in all_divs:
                imageLink = div.find("meta", {"property":"image"}).get("content")
                a = div.find("a", class_="product-title")
                productLink = "https://www.staples.ca" + a.get("href")
                productName = str(a.text).strip()
                subtitles = div.find("div", class_="product-subtitle")
                subtitle = str(subtitles.text)
                try:
                    modelNumberPro = subtitle.split("Model :", 1)[1].strip()
                except:
                    modelNumberPro = "none"
                span = div.find("span", {"property":"price"})
                productPrice = span.text
                with scrapingThread.addLock:
                    title.append(productName)
                    link.append(productLink)
                    images.append(imageLink)
                    modelNumber.append(modelNumberPro)
                    price.append(productPrice)
                print str(x) + str(productName)
                x = x + 1
                if x is 24:
                    print "Entered Here"
                    div2 = div.findAll("div", {"class":"stp--product-list"})
                    print div2
                    for div in div2:
                        imageLink = div.find("meta", {"property": "image"}).get("content")
                        a = div.find("a", class_="product-title")
                        productLink = "https://www.staples.ca" + a.get("href")
                        productName = str(a.text).strip()
                        subtitles = div.find("div", class_="product-subtitle")
                        subtitle = str(subtitles.text)
                        try:
                            modelNumberPro = subtitle.split("Model :", 1)[1].strip()
                        except:
                            modelNumberPro = "none"
                        span = div.find("span", {"property": "price"})
                        productPrice = span.text
                        with scrapingThread.addLock:
                            title.append(productName)
                            link.append(productLink)
                            images.append(imageLink)
                            modelNumber.append(modelNumberPro)
                            price.append(productPrice)
                        print str(x) + str(productName)
                        x = x + 1
        except Exception, e:
            PrintException()
            return

thread1 = scrapingThread()
thread2 = scrapingThread()
thread3 = scrapingThread()
thread1.start()
#thread2.start()
#thread3.start()

thread1.join()
#thread2.join()
#thread3.join()

df = pd.DataFrame()
df.insert(0, 'IDValues', range(0, len(title)))
df["Name"] = title
df["Price"] = price
df["link"] = link
df["ModelNumber"] = modelNumber
df["Image"] = images
df.to_csv("Staples.csv", index=False, encoding='utf-8')

