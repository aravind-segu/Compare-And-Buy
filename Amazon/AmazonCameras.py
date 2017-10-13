import random
import threading
import urllib2
import urllib
from time import sleep
from random import choice as rchoice
from bs4 import BeautifulSoup
import pandas as pd
import sys
import time
import urllib2
import pandas as pd
from selenium import webdriver
import requests
import pymysql

conn = pymysql.connect(host='localhost', user='root', db='productdata')
conn.set_charset('utf8')
cursor = conn.cursor()
sql = 'SELECT * from `cameras`;'
cursor.execute(sql)
countrow = cursor.execute(sql)
print countrow
links = []
images =[]
name = []
prices = []
x = 1
model = []
browser1 = webdriver.Chrome("../chromedriver.exe")
browser2 = webdriver.Chrome("../chromedriver.exe")
browser3 = webdriver.Chrome("../chromedriver.exe")
browser4 = webdriver.Chrome("../chromedriver.exe")
browserModel1 = webdriver.Chrome("../chromedriver.exe")
browserModel2 = webdriver.Chrome("../chromedriver.exe")
browserModel3 = webdriver.Chrome("../chromedriver.exe")
browserModel4 = webdriver.Chrome("../chromedriver.exe")
failedCount = 0
pageNumber = 0
class scrape():
    add_lock = threading.Lock()
    def findModel (self, link, threadNum):
        if threadNum is 1:
            browserGetModel = browserModel1
        if threadNum is 2:
            browserGetModel = browserModel2
        if threadNum is 3:
            browserGetModel = browserModel3
        if threadNum is 4:
            browserGetModel = browserModel4
        browserGetModel.get(link)
        html = browserGetModel.page_source
        soupTablet = BeautifulSoup(html)
        try:
            correctDiv = soupTablet.find("div", {"id": "detail_bullets_id"})
            Alli = correctDiv.findAll("li")
            for li in Alli:
                b = li.find("b")
                if not b:
                    continue
                if ("model number" in b.text):
                    modelNumber = li.text
                    return modelNumber[len(str(b.text)):]
                else:
                    continue
            return "none"
        except Exception as e:
            print e
            return "none"

    def getInformation(self, pageNumber, threadNum):
            try:
                counter = 0
                if threadNum is 1:
                    browserGetInfo = browser1
                if threadNum is 2:
                    browserGetInfo = browser2
                if threadNum is 3:
                    browserGetInfo = browser3
                if threadNum is 4:
                    browserGetInfo = browser4
                tabletUrl = "https://www.amazon.ca/s/ref=lp_677235011_pg_3?rh=n%3A667823011%2Cn%3A%21677211011%2Cn%3A677230011%2Cn%3A677235011&page=" + str(pageNumber) + "&ie=UTF8&qid=1501945050&spIA=B01G3PY7WM,B008GVXKUW,B00L8VYH86"

                time.sleep(3)
                browserGetInfo.get(tabletUrl)
                html = browserGetInfo.page_source
                soup = BeautifulSoup(html)
                all_ul = soup.find_all("ul",class_="s-result-list")
                print len(all_ul)
                for ul in all_ul:
                    for element in ul.find_all("li", class_="s-result-item"):
                        counter += 1
                        image = element.find("img")
                        if (image is None):
                            print("Entered")
                            continue
                        #print(image.get("src"))
                        #print (image.get("alt"))
                        productLink = element.find('a', class_='a-link-normal a-text-normal')
                        #print productLink.get("href")
                        priceSpan = element.find('span', class_='a-size-base a-color-price s-price a-text-bold')
                        if(priceSpan is None):
                            priceSpan = element.find('span', class_='a-size-base a-color-price a-text-bold')
                        price = priceSpan.find(text=True)
                        #print price
                        modelNumber = scrape.findModel(self,productLink.get("href"), threadNum)
                        print str(counter) + " " + productLink.get("href") + " " + modelNumber
                        with scrape.add_lock:
                            productName = image.get("alt")
                            link = productLink.get("href")
                            productImage = image.get("src")
                            vendor = "amazon"
                            print modelNumber
                            print productName
                            print link
                            print price
                            cursor.execute(
                                "INSERT into cameras(Name, Price, Link, ModelNumber, Images, Vendor) VALUES ('%s', '%s', '%s', '%s','%s', '%s')" % \
                                (productName, price, link, modelNumber, productImage, vendor))
                            model.append(modelNumber)
                            images.append(image.get("src"))
                            name.append(image.get("alt"))
                            links.append(productLink.get("href"))
                            prices.append(price)
                        if (counter is 24):
                            return "success"
                return "success"
            except urllib2.URLError as e:
                print (e.reason)
                return "failed"


while (pageNumber <= 25):
    sc = scrape()
    pageNumber += 1
    t1 = threading.Thread(target=scrape.getInformation, args = (sc,pageNumber,1,))
    pageNumber += 1
    t2 = threading.Thread(target=scrape.getInformation, args=(sc,pageNumber, 2,))
    pageNumber += 1
    t3 = threading.Thread(target=scrape.getInformation, args=(sc,pageNumber, 3,))
    pageNumber += 1
    t4 = threading.Thread(target=scrape.getInformation, args=(sc,pageNumber, 4,))
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()

print len (name)
print len(prices)
print len(links)
print len(images)
print len(model)
difference = len(name) - len(model)
while (difference > 0):
    model.append("none")
    difference -= 1
conn.commit()
conn.close()
df = pd.DataFrame()
df.insert(0, 'ID', range(0, len(name)))
df["Name"] = name
df["Price"] = prices
df["Link"] = links
df["Images"] = images
df["Model"] = model
print(df)
df.to_csv("AmazonCameras.csv",index=False, encoding='utf-8')
