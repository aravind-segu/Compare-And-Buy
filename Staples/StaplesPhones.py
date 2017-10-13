import linecache
import time
import urllib2
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import threading
import sys
import pymysql

conn = pymysql.connect(host='localhost', user='root', db='productdata')
conn.set_charset('utf8')
cursor = conn.cursor()
sql = 'SELECT * from `phones`;'
cursor.execute(sql)
countrow = cursor.execute(sql)
print(countrow)
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
        browser = webdriver.Chrome("../chromedriver.exe")
        browser.get("https://www.staples.ca")
        time.sleep(25)

        elem = browser.find_element_by_tag_name("body")

        no_of_pagedowns = 40

        while no_of_pagedowns:
            elem.send_keys(Keys.PAGE_DOWN)
            time.sleep(5)
            no_of_pagedowns -= 1

        html = browser.page_source
        soup = BeautifulSoup(html)
        self.getInformation(soup)
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
                    print productName
                    print productLink
                    print imageLink
                    print productPrice
                    vendor = "staples"
                    cursor.execute(
                        "INSERT into phones (Name, Price, Link, ModelNumber, Images, Vendor) VALUES('%s', '%s', '%s', '%s', '%s', '%s')" % (
                            productName, productPrice, productLink, modelNumberPro, imageLink, vendor))
                    title.append(productName)
                    link.append(productLink)
                    images.append(imageLink)
                    modelNumber.append(modelNumberPro)
                    price.append(productPrice)
                print str(x) + str(productName)
                x = x + 1
                # if x is 24:
                #     print "Entered Here"
                #     div2 = div.findAll("div", {"class":"stp--product-list"})
                #     print div2
                #     for div in div2:
                #         imageLink = div.find("meta", {"property": "image"}).get("content")
                #         a = div.find("a", class_="product-title")
                #         productLink = "https://www.staples.ca" + a.get("href")
                #         productName = str(a.text).strip()
                #         subtitles = div.find("div", class_="product-subtitle")
                #         subtitle = str(subtitles.text)
                #         try:
                #             modelNumberPro = subtitle.split("Model :", 1)[1].strip()
                #         except:
                #             modelNumberPro = "none"
                #         span = div.find("span", {"property": "price"})
                #         productPrice = span.text
                #         with scrapingThread.addLock:
                #             title.append(productName)
                #             link.append(productLink)
                #             images.append(imageLink)
                #             modelNumber.append(modelNumberPro)
                #             price.append(productPrice)
                #         print str(x) + str(productName)
                #         x = x + 1
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
conn.commit()
conn.close()

df = pd.DataFrame()
df.insert(0, 'IDValues', range(0, len(title)))
df["Name"] = title
df["Price"] = price
df["link"] = link
df["ModelNumber"] = modelNumber
df["Image"] = images
df.to_csv("StaplesPhones.csv", index=False, encoding='utf-8')

