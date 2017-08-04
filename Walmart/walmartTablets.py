import time
import urllib2
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

def findModel (productLink, browser):
    browser.get(productLink)
    time.sleep(1)
    html = browser.page_source
    soup = BeautifulSoup(html)
    Allspan = soup.find("span", {"itemprop":"model"})
    if not Allspan:
        return "none"
    else:
        return Allspan.text

price = []
title =[]
link = []
modelNumber = []
idNumber = []
threads = []
images = []

def getInformation(soup):
    allArticles = soup.findAll("article")
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
        productModel = findModel(productLink, browserModel)
        print productModel
        modelNumber.append(productModel)
        price.append(priceTag.text)
        title.append(productName)
        link.append(productLink)
        images.append(productImage)
browser = webdriver.Chrome("../chromedriver.exe")
browserModel = webdriver.Chrome("../chromedriver.exe")
browser.get("https://www.walmart.ca/en/electronics/ipad-tablets/apple-ipads/N-3468+1019767")
time.sleep(1)

html = browser.page_source
soup = BeautifulSoup(html)
getInformation(soup)
browser.get("https://www.walmart.ca/en/electronics/ipad-tablets/tablets/android-tablets/N-3467")
time.sleep(1)

html = browser.page_source
soupAndroid = BeautifulSoup(html)
getInformation(soupAndroid)
browser.get("https://www.walmart.ca/en/electronics/ipad-tablets/tablets/windows-tablets/N-3466")
time.sleep(1)

html = browser.page_source
soupWindows = BeautifulSoup(html)
getInformation(soupWindows)

df = pd.DataFrame()
df.insert(0, 'ID', range(0, len(title)))
df["Name"] = title
df["Price"] = price
df["Link"] = link
print len(modelNumber)
df["ModelNumber"] = modelNumber
df["Images"] = images
df.to_csv("walmartTablets.csv", index=False, encoding='utf-8')
