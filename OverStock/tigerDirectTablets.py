import urllib2
import threading
from bs4 import BeautifulSoup
import pandas as pd
import time
import requests

price = []
title =[]
linkList = []
modelNumber = []

def findModel(link):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    page = opener.open(link)
    soup = BeautifulSoup(page)
    tr = soup.find("td", {"itemprop":"mpn"})
    if not tr:
        return "none"
    else:
        return tr.text
class getPages:
    y = 0
    def getPage(self, pageNumber):
            try:
                opener = urllib2.build_opener()
                opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                url = "https://www.overstock.com/Electronics/Tablets/24821/subcat.html?index=" + str(pageNumber)
                page = opener.open(url)
                soup = BeautifulSoup(page)
                return soup
            except:
                y = -1
                return None

class scrapingThread (threading.Thread):
    pageNumber = 1
    page_lock = threading.Lock()
    add_lock = threading.Lock()
    gp = getPages()
    def _init_(self):
        super(scrapingThread, self).__init__()
    def run(self):
        while(True):
            with scrapingThread.page_lock:
                soup = getPages.getPage(self.gp,self.pageNumber)
                scrapingThread.pageNumber += 60
            response = self.getInformation(soup)
            print response
            if not response:
                break
    def getInformation(self, soup):
        x = 0
        try:
            all_products = soup.find_all("div" , class_="product-wrapper")
            for product in all_products:
                link = product.find("a")
                productLink = "https:" + str(link.get("href"))
                if productLink in link:
                    return "fail"
                productPrice = link.find("div", class_="product-price").text
                itemPrice = productPrice.split("Today: USD", 1)[1].strip()
                productTitle = link.find("div", class_="product-title").text
                modelName = findModel(productLink)
                with scrapingThread.add_lock:
                    price.append(itemPrice)
                    title.append(productTitle)
                    linkList.append(productLink)
                    modelNumber.append(modelName)
                x = x + 1
                print x
        except urllib2.URLError as e:
            return

y = 1

thread1 = scrapingThread()
thread2 = scrapingThread()
thread3 = scrapingThread()
thread1.start()
thread2.start()
thread3.start()
thread1.join()
thread2.join()
thread2.join()
df = pd.DataFrame()
print len(title)
print len(price)
print len(linkList)
print len(modelNumber)
df.insert(0, 'ID', range(0, len(title)))
df["Name"] = title
df["Price"] = price
df["Link"] = linkList
df["ModelNumber"] = modelNumber
print modelNumber
df.to_csv("OverStockTablet.csv",index=False, encoding='utf-8')

