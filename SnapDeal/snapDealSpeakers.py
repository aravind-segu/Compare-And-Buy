import threading
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
sql = 'SELECT * from `speakers`;'
cursor.execute(sql)
countrow = cursor.execute(sql)
print(countrow)
price = []
title =[]
link = []
modelNumber = []
image = []
threads = []
idNumber = []

def findModel (productLink,counter):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    page = opener.open(productLink)
    soup = BeautifulSoup(page)
    allTd = soup.findAll("td")
    found = False
    productModel = "none"
    for td in allTd:
        if ("Model Number" == td.text):
            print "entered"
            found = True
            continue
        if (found):
            productModel = td.text
            found = False
            break
    print str(counter) + productModel
    return productModel

browser = webdriver.Chrome("../chromedriver.exe")
browser.get("https://www.snapdeal.com/products/electronics-speakers?sort=plrty")
time.sleep(1)

elem = browser.find_element_by_tag_name("body")

no_of_pagedowns = 40

while no_of_pagedowns:
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(2)
    no_of_pagedowns-=1

html = browser.page_source
soup = BeautifulSoup(html)
all_elements = soup.findAll("div", {"class":"product-tuple-listing"})
print len(all_elements)
counter = 1
for element in all_elements:
    idNumber.append(counter)
    counter +=1
    aTag = element.find("a", {"class":"dp-widget-link"})
    productLink = aTag.get("href")
    prLink = str(productLink)
    imageTag = element.find("img")
    if not imageTag:
        productImage = "none"
    else:
        productImage = imageTag.get("src")
    nameTag = element.find("p", {"class": "product-title"})
    productName = nameTag.get("title")
    priceTag = element.find("span", {"class":"product-price"})
    productPrice = priceTag.get("data-price")
    productModel = findModel(productLink, counter)
    print productName
    print productPrice
    print productLink
    print productImage
    print productModel
    vendor = "snapdeal"
    cursor.execute(
        "INSERT into speakers(Name, Price, Link, ModelNumber, Images, Vendor) VALUES ('%s', '%s', '%s', '%s','%s', '%s')" % \
        (productName, priceTag.text.strip(), productLink, productModel, productImage, vendor))
    price.append(productPrice)
    title.append(productName)
    link.append(productLink)
    image.append(productImage)

conn.commit()
conn.close()
df = pd.DataFrame()
df.insert(0, 'ID', range(0, len(title)))
df["Name"] = title
df["Price"] = price
df["Link"] = link
print len(modelNumber)
df["ModelNumber"] = modelNumber
df["Images"] = image
df.to_csv("snapdealSpeakers.csv",index=False, encoding='utf-8')




