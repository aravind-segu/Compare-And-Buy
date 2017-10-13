import urllib2
import threading
from bs4 import BeautifulSoup
import pandas as pd
import time
import requests

price = []
title =[]
link = []
modelNumbers = []
idNumber = []
threads = []
image = []
import pymysql

conn = pymysql.connect(host='localhost', user='root', db='productdata')
conn.set_charset('utf8')
cursor = conn.cursor()
sql = 'SELECT * from `desktops`;'
cursor.execute(sql)
countrow = cursor.execute(sql)
print(countrow)
def findModel(link):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    page = opener.open(link)
    soup = BeautifulSoup(page)
    span = soup.find("span", {"id": "ctl00_CP_ctl00_PD_lblModelNumber"})
    imageDiv = soup.find("div", {"data-bby-media-container": "primaryMediaContainer"})
    # print imageDiv
    image = imageDiv.find("img")
    # print image
    print link + " " + image.get("src")
    image.append(image.get("src"))
    if not span:
        return ("none", image.get("src"))
    else:
        return (span.text, image.get("src"))
class getPages:
    y = 0
    def getPage(self, pageNumber):
            try:
                opener = urllib2.build_opener()
                opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                url = "http://www.bestbuy.ca/en-ca/category/desktop-computers/20213.aspx?type=product&page="+ str(pageNumber) +"&pageSize=64"
                print "entered"
                print url
                page = opener.open(url)
                soup = BeautifulSoup(page)
                print "entered"
                return soup
            except:
                y = -1
                return None

class scrapingThread (threading.Thread):
    pageNumber = 0
    page_lock = threading.Lock()
    add_lock = threading.Lock()
    gp = getPages()
    def _init_(self):
        super(scrapingThread, self).__init__()
    def run(self):
        while(True):
            with scrapingThread.page_lock:
                scrapingThread.pageNumber += 1
                soup = getPages.getPage(self.gp,self.pageNumber)
            all_ul = soup.find_all("ul", class_="listing-items util_equalheight clearfix")
            if not all_ul:
                break
            else:
                self.getInformation(soup)
    def getInformation(self, soup):
        x = 0
        try:
            all_ul = soup.find_all("ul" , class_="listing-items util_equalheight clearfix")
            if not all_ul:
                return
            for ul in all_ul:
                imageLink = ul.find("img")
                images = imageLink.get("src")
                for div in ul.findAll("div", {"class":"prod-info"}):
                    h4 = div.find("h4")
                    print h4.text
                    urlLink = ("http://www.bestbuy.ca" + h4.find("a").get("href"))
                    # model = findModel(urlLink)
                    with scrapingThread.add_lock:
                        modelNumber, images = findModel(urlLink)
                        name = h4.text
                        prices = div.find("span", {"class": "amount"}).text
                        print h4.text
                        print urlLink
                        print images
                        print modelNumber
                        print prices
                        vendor = "bestbuy"
                        cursor.execute(
                            "INSERT into desktops(Name, Price, Link, ModelNumber, Images, Vendor) VALUES ('%s', '%s', '%s', '%s','%s', '%s')" % \
                            (name, prices, urlLink, modelNumber, images, vendor))
                        image.append(images)
                        title.append(h4.text)
                        modelNumbers.append(modelNumber)
                        link.append(urlLink)
                        price.append(div.find("span", {"class": "amount"}).text)
                    print x
                    x = x + 1

        except urllib2.URLError as e:
            return

y = 1

thread1 = scrapingThread()
thread2 = scrapingThread()
thread3 = scrapingThread()
thread4 = scrapingThread()
thread5 = scrapingThread()
thread6 = scrapingThread()
thread7 = scrapingThread()
thread8 = scrapingThread()
thread9 = scrapingThread()
thread10 = scrapingThread()
thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread5.start()
thread6.start()
thread7.start()
thread8.start()
thread9.start()
thread10.start()
thread1.join()
thread2.join()
thread3.join()
thread4.join()
thread5.join()
thread6.join()
thread7.join()
thread8.join()
thread9.join()
thread10.join()
conn.commit()
conn.close()
df = pd.DataFrame()
df.insert(0, 'ID', range(0, len(title)))
df["Name"] = title
df["Price"] = price
df["Link"] = link
df["ModelNumber"] = modelNumbers
df["Images"] = image
print modelNumbers
df.to_csv("BestBuyDesktops.csv",index=False, encoding='utf-8')

