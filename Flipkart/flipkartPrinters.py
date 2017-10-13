import linecache
import urllib2
import threading
from bs4 import BeautifulSoup
import pandas as pd
import requests
import sys
priceList = []
title =[]
linkList = []
modelNumber = []
import pymysql

conn = pymysql.connect(host='localhost', user='root', db='productdata')
conn.set_charset('utf8')
cursor = conn.cursor()
sql = 'SELECT * from `printers`;'
cursor.execute(sql)
countrow = cursor.execute(sql)

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)

def findModel(link):
    try:
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        page = opener.open(link)
        soup = BeautifulSoup(page)
        Allli = soup.findAll("li", {"class": "_1KuY3T"})
        modelNumber = "none"
        for li in Allli:
            div = li.find("div", {"class":"col-3-12"})
            if div.text == "Model Number":
                correctli = li.find("li", {"class": "sNqDog"})
                modelNumber = correctli.text
            else:
                continue
        return modelNumber
    except Exception as e:
        return "none"
class getPages:
    y = 0
    def getPage(self, pageNumber):
            try:
                url = "https://www.flipkart.com/computers/computer-peripherals/printers-inks/printers/pr?otracker=categorytree&page=" + str(pageNumber) + "&sid=6bo%2Ctia%2Cffn%2Ct64&viewType=grid"
                print url
                r = requests.get(url)
                content = r.content.decode(encoding='UTF-8')
                soup = BeautifulSoup(r.content.decode(encoding='UTF-8'), "lxml")
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
            allProducts = soup.findAll("div", {"class": "_2-gKeQ"})
            if not allProducts:
                break
            else:
                self.getInformation(soup)
    def getInformation(self,soup):
        x = 0
        try:
            divs = soup.findAll("div", {"class": "_2-gKeQ"})
            for div in divs:
                link = div.find("a")
                productLink = "https://www.flipkart.com" + str(link.get("href"))
                name = div.find("div", "_3wU53n")
                productName = name.text
                price = div.find("div", "_1vC4OE")
                if not price:
                    continue
                productPrice = price.text
                print productLink
                print productName
                print productPrice
                productModel = findModel(productLink)
                with scrapingThread.add_lock:
                    productImage = "https://fastandfriendly.us/wp-content/uploads/2017/07/IMAGE-COMING-SOON.png"
                    vendor = "flipkart"
                    cursor.execute(
                        "INSERT into printers(Name, Price, Link, ModelNumber, Images, Vendor) VALUES ('%s', '%s', '%s', '%s','%s', '%s')" % \
                        (productName, productPrice, productLink, productModel, productImage, vendor))
                    priceList.append(productPrice)
                    title.append(productName)
                    linkList.append(productLink)
                    modelNumber.append(productModel)
                x = x + 1
                print x
        except Exception as e:
            PrintException()

thread1 = scrapingThread()
thread2 = scrapingThread()
thread3 = scrapingThread()
thread4 = scrapingThread()
thread5 = scrapingThread()
thread6 = scrapingThread()
thread7 = scrapingThread()
thread8 = scrapingThread()
thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread5.start()
thread6.start()
thread7.start()
thread8.start()
thread1.join()
thread2.join()
thread3.join()
thread4.join()
thread5.join()
thread6.join()
thread7.join()
thread8.join()

conn.commit()
conn.close()
df = pd.DataFrame()
df.insert(0, 'ID', range(0, len(title)))
df["Name"] = title
df["Price"] = priceList
df["Link"] = linkList
df["ModelNumber"] = modelNumber
df.to_csv("FlipkartSpeakes.csv",index=False, encoding='utf-8')