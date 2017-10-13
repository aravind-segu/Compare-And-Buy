import time
import urllib2
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import threading
price = []
title =[]
link = []
modelNumber = []
idNumber = []
threads = []
images = []
import pymysql

conn = pymysql.connect(host='localhost', user='root', db='productdata')
conn.set_charset('utf8')
cursor = conn.cursor()
sql = 'SELECT * from `speakers`;'
cursor.execute(sql)
countrow = cursor.execute(sql)
print(countrow)

class scrape():
    add_lock = threading.Lock()
    def findModel (self,productLink, threadNum):
        if threadNum is 1:
            browser = browserModel1
        if threadNum is 2:
            browser = browserModel2
        if threadNum is 3:
            browser = browserModel3
        if threadNum is 4:
            browser = browserModel4
        # if threadNum is 5:
        #     browser = browserModel5
        browser.get(productLink)
        time.sleep(1)
        html = browser.page_source
        soup = BeautifulSoup(html)
        Allspan = soup.find("span", {"itemprop":"model"})
        if not Allspan:
            return "none"
        else:
            return Allspan.text

    def getInformation(self, pageNumber, threadNum):
        if threadNum is 1:
            browser = browser1
        if threadNum is 2:
            browser = browser2
        if threadNum is 3:
            browser = browser3
        if threadNum is 4:
            browser = browser4
        # if threadNum is 5:
        #     browser = browser5
        browser.get("https://www.walmart.ca/en/electronics/audio/audio-speakers/N-4254/page-" + str(pageNumber))

        time.sleep(1)
        html = browser.page_source
        soup = BeautifulSoup(html)
        allArticles = soup.findAll("article", {"class":"standard-thumb"})
        print "entered"
        print len(allArticles)
        count = 0
        for article in allArticles:
            imageTag = article.find("img")
            productImage = "https:" + str(imageTag.get("src"))
            productName =  imageTag.get("alt")
            linkTag = article.find("a")
            productLink = "https://www.walmart.ca" + str(linkTag.get("href"))
            priceTag = article.find("div", {"class":"price-current"})
            # print priceTag.text
            # print productLink
            # print productName
            # print productImage
            productModel = scrape.findModel(self,productLink, threadNum)
            print str(count) + " " + productModel
            count += 1
            with scrape.add_lock:
                vendor = "walmart"
                try:
                    cursor.execute(
                        "INSERT into speakers(Name, Price, Link, ModelNumber, Images, Vendor) VALUES ('%s', '%s', '%s', '%s','%s', '%s')" % \
                        (productName, priceTag.text.strip(), productLink, productModel, productImage, vendor))
                except:
                    print "SQL Exception"
                    continue

                modelNumber.append(productModel)
                price.append(priceTag.text)
                title.append(productName)
                link.append(productLink)
                images.append(productImage)

sc = scrape()
browser1 = webdriver.Chrome("../chromedriver.exe")
browser2 = webdriver.Chrome("../chromedriver.exe")
browser3 = webdriver.Chrome("../chromedriver.exe")
browser4 = webdriver.Chrome("../chromedriver.exe")
browserModel1 = webdriver.Chrome("../chromedriver.exe")
browserModel2 = webdriver.Chrome("../chromedriver.exe")
browserModel3 = webdriver.Chrome("../chromedriver.exe")
browserModel4 = webdriver.Chrome("../chromedriver.exe")
sc = scrape()
t1 = threading.Thread(target=scrape.getInformation, args=(sc, 1, 1,))
t2 = threading.Thread(target=scrape.getInformation, args=(sc, 2, 2,))
t3 = threading.Thread(target=scrape.getInformation, args=(sc, 3, 3,))
t4 = threading.Thread(target=scrape.getInformation, args=(sc, 4, 4,))
t1.start()
t2.start()
t3.start()
t4.start()
t1.join()
t2.join()
t3.join()
t4.join()

conn.commit()
conn.close()
df = pd.DataFrame()
df["Name"] = title
df["Price"] = price
df["Link"] = link
print len(modelNumber)
df["ModelNumber"] = modelNumber
df["Images"] = images
oldSpeakers = pd.read_csv("walmartSpeakers.csv")
oldTitle = oldSpeakers["Name"]
oldSpeakers = oldSpeakers.drop('ID', axis=1)
frame = [oldSpeakers, df]
master = pd.concat(frame)
master.insert(0, 'ID', range(0, len(title) + len(oldTitle)))
master.to_csv("walmartSpeakers.csv",index=False, encoding='utf-8')

