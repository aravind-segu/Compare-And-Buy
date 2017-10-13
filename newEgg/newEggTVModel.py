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
reload(sys)
sys.setdefaultencoding('utf-8')


browser1 = webdriver.Chrome("../chromedriver.exe")
browser2 = webdriver.Chrome("../chromedriver.exe")
browser3 = webdriver.Chrome("../chromedriver.exe")
browser4 = webdriver.Chrome("../chromedriver.exe")
browser5 = webdriver.Chrome("../chromedriver.exe")
# browser6 = webdriver.Chrome("../chromedriver.exe")
# browser7 = webdriver.Chrome("../chromedriver.exe")
# browser8 = webdriver.Chrome("../chromedriver.exe")
# browser9 = webdriver.Chrome("../chromedriver.exe")
# browser10 = webdriver.Chrome("../chromedriver.exe")
# browser11 = webdriver.Chrome("../chromedriver.exe")
# browser12 = webdriver.Chrome("../chromedriver.exe")
dictModel = {}
class scrape:
    def getInformation(self, link, name, threadNum, sleepTime,i):
        try:
            if threadNum is 1:
                browserGetInfo = browser1
            if threadNum is 2:
                browserGetInfo = browser2
            if threadNum is 3:
                browserGetInfo = browser3
            if threadNum is 4:
                browserGetInfo = browser4
            if threadNum is 5:
                browserGetInfo = browser5
            # if threadNum is 6:
            #     browserGetInfo = browser6
            # if threadNum is 7:
            #     browserGetInfo = browser7
            # if threadNum is 8:
            #     browserGetInfo = browser8
            # if threadNum is 9:
            #     browserGetInfo = browser9
            # if threadNum is 10:
            #     browserGetInfo = browser10
            # if threadNum is 11:
            #     browserGetInfo = browser11
            # if threadNum is 12:
            #     browserGetInfo = browser12
            time.sleep(sleepTime)
            browserGetInfo.get(link)
            html = browserGetInfo.page_source
            soup = BeautifulSoup(html)
            correctDiv = soup.find("div", {"id": "Specs"})
            fieldSet = correctDiv.find("fieldset")
            if not fieldSet:
                dictModel[link] = "none"
                return
            dls = fieldSet.findAll("dl")
            if not dls:
                dictModel[link] = "none"
                return
            productModel = "none"
            for dl in dls:
                dt = dl.find("dt")
                if (dt.text == "Model"):
                    productModel = dl.find("dd").text
                else:
                    continue
            print name + " " + productModel
            dictModel[link] = productModel
        except:
            printException()
            if (i <= 5):
                self.getInformation(link, name, threadNum, 10,i)
            else:
                dictModel[link] = "none"
                return

def printException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)


newEgg = pd.read_csv("./newEggTVs.csv")
print newEgg.columns.values
linkList = newEgg["Link"]
names = newEgg["Name"]
print linkList[0]
i = 0
while i < 279:
    sc = scrape()
    print "testing " + str(i)+ names[i]
    t1 = threading.Thread(target=scrape.getInformation, args=(sc, linkList[i],names[i], 1, 1,i,))
    i += 1
    if (i > 279):
        break
    print "testing " + str(i) + names[i]
    t2 = threading.Thread(target=scrape.getInformation,  args=(sc, linkList[i],names[i], 2,1,i,))
    i += 1
    if (i > 279):
        break
    print "testing " + str(i) + names[i]
    t3 = threading.Thread(target=scrape.getInformation, args=(sc, linkList[i],names[i], 3,1,i,))
    i += 1
    if (i > 279):
         break
    print "testing " + str(i) + names[i]
    t4 = threading.Thread(target=scrape.getInformation, args=(sc, linkList[i],names[i], 4,1,i,))
    i += 1
    if (i > 279):
        break
    print "testing " + str(i) + names[i]
    t5 = threading.Thread(target=scrape.getInformation, args=(sc, linkList[i], names[i],5,1,i,))
    i += 1
    if (i > 279):
        break
    # print "testing " + str(i) + names[i]
    # t6 = threading.Thread(target=scrape.getInformation, args=(sc, linkList[i], names[i],6,1,i,))
    # i += 1
    # if (i > 100):
    #     break
    # t7 = threading.Thread(target=scrape.getInformation, args=(sc, linkList[i], 7,))
    # i += 1
    # if (i > len(linkList)):
    #     break
    # t8 = threading.Thread(target=scrape.getInformation, args=(sc, linkList[i], 8,))
    # i += 1
    # if (i > len(linkList)):
    #     break
    # t9 = threading.Thread(target=scrape.getInformation, args=(sc, linkList[i], 9,))
    # i += 1
    # if (i > len(linkList)):
    #     break
    # t10 = threading.Thread(target=scrape.getInformation, args=(sc, linkList[i], 10,))
    # i += 1
    # if (i > len(linkList)):
    #     break
    # t11 = threading.Thread(target=scrape.getInformation, args=(sc, linkList[i], 11,))
    # i += 1
    # if (i > len(linkList)):
    #     break
    # t12 = threading.Thread(target=scrape.getInformation, args=(sc, linkList[i], 12,))
    # i += 1
    # if (i > len(linkList)):
    #     break
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    # t6.start()
    # t7.start()
    # t8.start()
    # t9.start()
    # t10.start()
    # t11.start()
    # t12.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    # t6.join()
    # t7.join()
    # t8.join()
    # t9.join()
    # t10.join()
    # t11.join()
    # t12.join()

modelNumber = []
for d in dictModel:
    print d + " " + dictModel[d]
for link in newEgg["Link"]:
    if link in dictModel:
        modelNumber.append(dictModel[link])
    else:
        modelNumber.append("none")
newEgg.insert(2, 'ModelNumber', modelNumber)
newEgg.to_csv("newEggTvModel.csv",index=False, encoding='utf-8')