import pandas as pd
import sys
import operator
from bs4 import BeautifulSoup
import urllib2
import pymysql
import sys
from operator import itemgetter
reload(sys)
sys.setdefaultencoding("utf-8")

conn = pymysql.connect(host='localhost', user='root', db='productdata')
conn.set_charset('utf8')
cursor = conn.cursor()

tabletsRelease = pd.read_sql("SELECT * FROM televisioncombination ORDER BY Rating ASC", con=conn)

def getTVs():
    tabletsList = []
    count = 0
    for j, row in tabletsRelease.iterrows():
        idNumber = row[0]
        count += 1
        indTablets = []
        duplicateDict = {}
        products = pd.read_sql("SELECT * FROM television WHERE tvMapping = %(idValue)s", con = conn, params = {"idValue":idNumber})
        for j, row in products.iterrows():
            dict = {}
            rawPrice = ""
            finalPrice = ""
            try:
                if (row[6] == "flipkart" or row[6] == "snapdeal"):
                    aInt = int(filter(str.isdigit, row[2]))
                    dolPrice = round(aInt * 0.019, 2)
                    rawPrice = dolPrice
                    dolPrice = "${:,.2f}".format(dolPrice)
                    finalPrice = dolPrice
                else:
                    if '.' in row[2]:
                        aInt = int(filter(str.isdigit, row[2]))
                        aInt = aInt * 0.01
                        rawPrice = aInt
                        aInt = "${:,.2f}".format(aInt)
                        finalPrice = aInt
                    else:
                        aInt = int(filter(str.isdigit, row[2]))
                        rawPrice = aInt
                        aInt = "${:,.2f}".format(aInt)
                        finalPrice = aInt
                if (finalPrice in duplicateDict):
                    vendor = duplicateDict.get(finalPrice)
                    if (vendor == row[6]):
                        print("product skipped")
                        continue
                duplicateDict[finalPrice] = row[6]
                dict["rawPrice"] = rawPrice
                dict["Price"] = finalPrice
            except:
                print ("product skipped")
                continue
            dict["Name"] = row[1]
            dict["Image"] = row[5]
            dict["Link"] = row[3]
            dict["Website"] = row[6]
            indTablets.append(dict)
        indTablets = sorted(indTablets, key=itemgetter('rawPrice'))
        tabletsList.append(indTablets)
    return tabletsList
def getTVsPage(tabletsList, pageNumber):
    if pageNumber == 1:
        return tabletsList[0:10]
    lowIndex = ((pageNumber - 1) * 10) + 1
    highIndex = pageNumber * 10
    return tabletsList[lowIndex:highIndex]

def getMaxPageTV(tabletsList):
    return len(tabletsList)/10

getTVs()