import linecache
import urllib2
import threading
from bs4 import BeautifulSoup
import pandas as pd
import requests
import sys
import time
import urllib2
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pymysql

conn = pymysql.connect(host='localhost', user='root', db='productdata')
conn.set_charset('utf8')
cursor = conn.cursor()
sql = 'SELECT * from `laptops`;'
cursor.execute(sql)
countrow = cursor.execute(sql)
print(countrow)
reload(sys)
sys.setdefaultencoding('utf-8')

price = []
title = []
link = []
modelNumber = []
images = []
brand = []
series = []
browser1 = webdriver.Chrome("../chromedriver.exe")
browser2 = webdriver.Chrome("../chromedriver.exe")
browser3 = webdriver.Chrome("../chromedriver.exe")
browser4 = webdriver.Chrome("../chromedriver.exe")
pageNumber = 0
def printException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)

def findModel(link):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    page = opener.open(link)
    soup = BeautifulSoup(page)
    correctDiv = soup.find("div", {"id":"Specs"})
    fieldSet = correctDiv.find("fieldset")
    dls = fieldSet.findAll("dl")
    productBrand = "none"
    productSeries = "none"
    productModel = "none"
    for dl in dls:
        dt = dl.find("dt")
        if (dt.text == "Brand"):
            productBrand = dl.find("dd").text
        elif (dt.text == "Series"):
            productSeries = dl.find("dd").text
        elif (dt.text == "Model"):
            productModel = dl.find("dd").text
        else:
            break
    specs = []
    specs.append(productBrand)
    specs.append(productSeries)
    specs.append(productModel)
    return specs



class scrape ():
    add_lock = threading.Lock()
    def getInformation(self, pageNumber, threadNum):
        # # opener = urllib2.build_opener()
        # # opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        # url = "https://www.newegg.ca/Tablets/SubCategory/ID-2557/Page-" + str(
        #      pageNumber) + "?Tid=165903&PageSize=36&order=BESTMATCH"
        # # print url
        # # # page = opener.open(url)
        # # urlFile = "./newEgg" + str(pageNumber) + ".html"
        # # print urlFile
        # # soup = BeautifulSoup(open(urlFile))
        # # print "got here"
        x = 0
        # browser.get(url)
        # time.sleep(1)
        # html = browser.page_source
        # soup = BeautifulSoup(html)
        try:
            if threadNum is 1:
                browserGetInfo = browser1
            if threadNum is 2:
                browserGetInfo = browser2
            if threadNum is 3:
                browserGetInfo = browser3
            if threadNum is 4:
                browserGetInfo = browser4
            url = "https://www.newegg.ca/Laptops-Notebooks/SubCategory/ID-32/Page-" + str(pageNumber) + "?Tid=6741&PageSize=96&order=BESTMATCH"
            browserGetInfo.get(url)
            time.sleep(20)
            html = browserGetInfo.page_source
            soup = BeautifulSoup(html)
            allDivs = soup.findAll("div", {"class": "item-container"})
            if not allDivs:
                scrape.getInformation(self,pageNumber,threadNum)
            print len(allDivs)
            for div in allDivs:
                print"Entered"
                imageTab = div.find("img")
                image = imageTab.get("src")
                productName = imageTab.get("title")
                if (title == productName):
                    return "fail"
                # print image
                # print productName
                correctLink = div.find("a", {"title":"View Details"})
                productLink = correctLink.get("href")
                # print productLink
                try:
                    priceSpan = div.find("li", {"class":"price-current"})
                    if not priceSpan:
                        continue
                    strong = priceSpan.find("strong")
                    sup = priceSpan.find("sup")
                    totalPrice = strong.text + sup.text
                except:
                    continue
                try:
                    modelUL = div.find("ul", {"class": "item-features"})
                    childLi = modelUL.findAll("li")
                    productModel = "none"
                    for li in childLi:
                        if ("model" in str(li.find("strong").text).lower()):
                            productModel = li.text
                            productModel = productModel.replace("Model #: ", "")
                            print productModel
                            break
                except:
                    continue
                # print totalPrice
                # print x
                # print
                # print
                #specs = findModel(productLink)
                print "entered adding"
                print productName
                with scrape.add_lock:
                    vendor = "newegg"
                    # productModel = "none"
                    cursor.execute(
                        "INSERT into laptops(Name, Price, Link, ModelNumber, Images, Vendor) VALUES ('%s', '%s', '%s', '%s','%s', '%s')" % \
                        (productName, totalPrice, productLink, productModel, image, vendor))
                    title.append(productName)
                    link.append(productLink)
                    price.append(totalPrice)
                    images.append(image)
                # brand.append(specs [0])
                # series.append(specs [1])
                # modelNumber.append(specs[2])
                x = x + 1
                print str(x) + "   " + str(productName)
                print
            return "success"
        except:
            printException()
while (pageNumber <= 30):
    sc = scrape()
    pageNumber += 1
    if (pageNumber > 30):
        break
    t1 = threading.Thread(target=scrape.getInformation, args=(sc, pageNumber, 1,))
    pageNumber += 1
    if (pageNumber > 30):
        break
    t2 = threading.Thread(target=scrape.getInformation, args=(sc, pageNumber, 2,))
    pageNumber += 1
    if (pageNumber > 30):
        break
    t3 = threading.Thread(target=scrape.getInformation, args=(sc, pageNumber, 3,))
    pageNumber += 1
    if (pageNumber > 30):
        break
    t4 = threading.Thread(target=scrape.getInformation, args=(sc, pageNumber, 4,))
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()

# broswer1 = webdriver.Chrome("../chromedriver.exe")
# browser2 = webdriver.Chrome("../chromedriver.exe")
# thread1 = scrapingThread()
# scrapingThread.setBrowser(thread1,broswer1)
# thread1.start()
#
#
# # thread3 = scrapingThread()
# # thread4 = scrapingThread()
# # thread5 = scrapingThread()
# # thread6 = scrapingThread()
# # thread7 = scrapingThread()
# # thread8 = scrapingThread()
# # thread9 = scrapingThread()
# # thread10 = scrapingThread()
# # thread3.start()
# # thread4.start()
# # thread5.start()
# # thread6.start()
# # thread7.start()
# # thread8.start()
# # thread9.start()
# # thread10.start()
# thread1.join()
# print"EnteredJoin"
# # thread3.join()
# # thread4.join()
# # thread5.join()
# # thread6.join()
# # thread7.join()
# # thread8.join()
# # thread9.join()
# # thread10.join()
conn.commit()
conn.close()
df = pd.DataFrame()
df.insert(0, 'ID', range(0, len(title)))
df["Name"] = title
df["Price"] = price
df["Link"] = link
# df["ModelNumber"] = modelNumber
df["Images"] = images
# df["Brand"] = brand
# df["Series"] = series
df.to_csv("newEggLaptops.csv",index=False, encoding='utf-8')