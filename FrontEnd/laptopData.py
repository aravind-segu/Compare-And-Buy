import pandas as pd
import pymysql
import sys
from operator import itemgetter
reload(sys)
sys.setdefaultencoding("utf-8")

conn = pymysql.connect(host='localhost', user='root', db='productdata')
conn.set_charset('utf8')
cursor = conn.cursor()

# The laptopsCombination is sorted and inserted as a dataframe
laptopsRelease = pd.read_sql("SELECT * FROM laptopcombination ORDER BY Rating ASC", con=conn)

def getLaptops():
    laptopsList = []
    count = 0
    # For each row in laptopsRelease
        # products are extracted from the laptops table
    for j, row in laptopsRelease.iterrows():
        idNumber = row[0]
        count += 1
        indLaptops = []
        duplicateDict = {}
        products = pd.read_sql("SELECT * FROM laptops WHERE laptopMapping = %(idValue)s", con = conn, params = {"idValue":idNumber})
        for j, row in products.iterrows():
            # The prices are retrieved and formatted correctly for display
            # A dictionary is intialized and all the details are stored in the dictionary
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
            indLaptops.append(dict)
        # The dictionaries are sorted by the price and then appended to the productList
        indLaptops = sorted(indLaptops, key=itemgetter('rawPrice'))
        laptopsList.append(indLaptops)
    return laptopsList

# The approprate set of 10 are extracted and returned to the controller.py
def getLaptopsPage(tabletsList, pageNumber):
    if pageNumber == 1:
        return tabletsList[0:10]
    lowIndex = ((pageNumber - 1) * 10) + 1
    highIndex = pageNumber * 10
    return tabletsList[lowIndex:highIndex]

# Returns the maximum pages needed for the product List
def getMaxPageLaptop(tabletsList):
    return len(tabletsList)/10

getLaptops()