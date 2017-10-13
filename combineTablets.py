import csv
import threading

import pandas as pd
from fuzzywuzzy import fuzz
import pymysql

conn = pymysql.connect(host='localhost', user='root', db='productdata')
conn.set_charset('utf8')
cursor = conn.cursor()
sql = 'SELECT * from `tablets`;'
cursor.execute(sql)
countrow = cursor.execute(sql)
print(countrow)

# bestBuy = pd.read_csv("./BestBuy/BestBuy.csv")
# print bestBuy.columns.values
# bestBuy["name"] = "bestbuy"
# print bestBuy.head()
# print bestBuy.shape

combinedData = pd.read_sql("SELECT * FROM tablets", con= conn)

bestBuy = pd.read_sql("SELECT * FROM tablets WHERE VENDOR='bestbuy'", con= conn)
print bestBuy.shape

amazon = pd.read_sql("SELECT * FROM tablets WHERE VENDOR='amazon'", con= conn)
print amazon.shape

newEgg = pd.read_sql("SELECT * FROM tablets WHERE VENDOR='newegg'", con= conn)
print newEgg.shape

flipkart = pd.read_sql("SELECT * FROM tablets WHERE VENDOR='flipkart'", con= conn)
print flipkart.shape

snapDeal = pd.read_sql("SELECT * FROM tablets WHERE VENDOR='snapdeal'", con= conn)
print snapDeal.shape

staples = pd.read_sql("SELECT * FROM tablets WHERE VENDOR='staples'", con= conn)
print staples.shape

walmart = pd.read_sql("SELECT * FROM tablets WHERE VENDOR='walmart'", con= conn)
print walmart.shape

def priceCorrection(dataset):
    newPriceBestBuy= []
    for price in dataset["Price"]:
        try:
            aInt = int(filter(str.isdigit, price))
        except:
            print "wrong price"
            aInt = 0
        if ("." in str(price)):
            newPriceBestBuy.append(aInt * 0.01)
        else:
            newPriceBestBuy.append(aInt)
    dataset.drop('Price', axis=1, inplace= True)
    dataset.insert(4, "Price", newPriceBestBuy)

priceCorrection(bestBuy)
priceCorrection(amazon)
priceCorrection(newEgg)
priceCorrection(staples)
priceCorrection(walmart)

dollars = []
for price in snapDeal["Price"]:
    aInt = int(filter(str.isdigit, price))
    dollars.append(round(aInt * 0.019,2))
snapDeal.drop('Price', axis=1, inplace= True)
snapDeal.insert(4, "Price", dollars)

dollars = []
for price in flipkart["Price"]:
    aInt = int(filter(str.isdigit, price))
    dollars.append(round(aInt * 0.019,2))
flipkart.drop('Price', axis=1, inplace= True)
flipkart.insert(4, "Price", dollars)

print flipkart.head()
combinedDataset = [bestBuy, amazon, newEgg, staples, walmart, flipkart, snapDeal]
brands = []
brands.append("samsung")
brands.append("apple")
brands.append("hp")
brands.append("asus")
brands.append("acer")
brands.append("lg")
brands.append("microsoft")
brands.append("lenovo")
brands.append("polaroid")
brands.append("other")

def identifyBrand(brands, dataset):
    company = []
    notFound = True
    counter = 0
    for name in dataset["Name"]:
        counter += 1
        for brand in brands:
            if brand in name.lower():
                company.append(brand)
                notFound = False
                break
        if notFound:
            company.append("other")
        notFound = True
    dataset.insert(5, "Company", company)

identifyBrand(brands, bestBuy)
identifyBrand(brands, amazon)
identifyBrand(brands, newEgg)
identifyBrand(brands, flipkart)
identifyBrand(brands, staples)
identifyBrand(brands, walmart)
identifyBrand(brands, snapDeal)


def groupByBrand(combinedDataset , d, companyNames, brandName):
    i = 0
    for dataset in combinedDataset:
        name = dataset.groupby("Company")
        try:
            name.get_group(name=brandName)
            d["{0}Data".format(companyNames[i])] = pd.DataFrame
            print brandName + str(len(name.get_group(name=brandName)))
            d["{0}Data".format(companyNames[i])] = name.get_group(name=brandName)
            print d["{0}Data".format(companyNames[i])].head()
            print d["{0}Data".format(companyNames[i])].shape
            i += 1
        except KeyError as e:
            i+=1
            continue

dSamsung = {}
dApple = {}
dHp = {}
dAsus = {}
dAcer = {}
dLg = {}
dMicrosoft = {}
dLenovo = {}
dPolaroid = {}
dOther = {}
combinedBrandDataset = [dSamsung, dApple, dHp, dAsus, dAcer, dLg, dMicrosoft, dLenovo, dPolaroid, dOther]
companyNames = []
companyNames.append("bestbuy")
companyNames.append("amazon")
companyNames.append("newEgg")
companyNames.append("staples")
companyNames.append("walmart")
companyNames.append("flipkart")
companyNames.append("snapDeal")

groupByBrand(combinedDataset, dSamsung, companyNames, "samsung")
groupByBrand(combinedDataset, dApple, companyNames, "apple")
groupByBrand(combinedDataset, dHp, companyNames, "hp")
groupByBrand(combinedDataset, dAsus, companyNames, "asus")
groupByBrand(combinedDataset, dAcer, companyNames, "acer")
groupByBrand(combinedDataset, dLg, companyNames, "lg")
groupByBrand(combinedDataset, dMicrosoft, companyNames, "microsoft")
groupByBrand(combinedDataset, dLenovo, companyNames, "lenovo")
groupByBrand(combinedDataset, dPolaroid, companyNames, "polaroid")
groupByBrand(combinedDataset, dOther, companyNames, "other")
print "starting"

print combinedDataset
threads = []
def checkEquality (name1, name2, price1,price2, countSame,vendor):
    similarity = fuzz.token_set_ratio(name1, name2)
    if (vendor != "flipkart" and vendor != "snapdeal"):
        try:
            modPrice = int(filter(str.isdigit, price2))
        except:
            print "wrong price"
            modPrice = 0
        if ("." in str(price2)):
            modPrice = (modPrice * 0.01)
    else:
        modPrice = int(filter(str.isdigit, price2))
        modPrice = (round(modPrice * 0.019, 2))
    # if (similarity > 85):
    #     print str(countSame) + " Similarity: " + str(similarity) + " " + name1 + " " + name2
    #     return True
    # else:
    #     return False
    if (similarity > 85):
        if (abs(modPrice - price1) < 250.0):
            print str(countSame) + " Similarity: " + str(similarity) + " " + name1 + " " + name2
            return True
        else:
            print ("Entered false price")
            print (name1)
            print (name2)
            print (price1)
            print (modPrice)
            return False
    else:
        return False
combinedMaster = []
def comparePlain (combinedPlain, master):
    print len(combinedPlain)
    print combinedPlain
    print len(master)
    print master
    count = 0
    found = False
    for dataset in combinedPlain:
        for i, row in dataset.iterrows():
            for modelNumber in master.keys():
                count += 1
                productID = master[modelNumber][0]
                rowName = combinedData[combinedData.ID == productID].Name.item()
                rowPrice = combinedData[combinedData.ID == productID].Price.item()
                rowVendor = combinedData[combinedData.ID == productID].Vendor.item()
                if (checkEquality(rowName, row["Name"], row["Price"], rowPrice, count, rowVendor)):
                    productDetails = master[modelNumber]
                    productDetails.append(row["ID"])
                    master[modelNumber] = productDetails
                    found = True
                    break
            if found == False:
                print count
                print "Entered"
                productDetails = []
                productDetails.append(row["ID"])
                master[row["Name"]] = productDetails
            found = False
    print count
    print "Final Master Length: " + str(len(master))
    print "printing master"
    print master
    combinedMaster.append(master)
for dBrand in combinedBrandDataset:
    combinedPlain = []
    master = {}
    for data in dBrand:
           if ("newEgg" in data):
               print "entered"
           d = dBrand[data]
           print d.shape
           dPlain = d[d["ModelNumber"] == "none"]
           print dPlain.shape
           dModelNumber = d[d["ModelNumber"] != "none"]
           print dModelNumber.shape
           combinedPlain.append(dPlain)
           for i, row in dModelNumber.iterrows():
               if row['ModelNumber'].strip() in master:
                   productDetails = master[row['ModelNumber'].strip()]
                   productDetails.append(row["ID"])
               else:
                   productDetails = []
                   productDetails.append(row["ID"])
                   master[row["ModelNumber"].strip()] = productDetails
           print "Master Length: " + str(len(master))
    print master
    print len(master)
    print len(combinedPlain)
    t1 = threading.Thread(target=comparePlain, args=(combinedPlain,master))
    t1.start()
    threads.append(t1)


for thread in threads:
    thread.join()

laptopMaster = {}
for masterDict in combinedMaster:
    IDMapping = {}
    for key in masterDict:
        productIDs = masterDict[key]
        rating = 2
        if (len(productIDs) > 2):
            rating = 1
        try:
            cursor.execute(
                "INSERT into tabletscombination(Name,Rating) VALUES ('%s', '%s')" % \
                (key, rating))
        except:
            print "error while inserting into tabletscombo"
            continue
        IDMapping[key] = cursor.lastrowid
    conn.commit()
    for key in masterDict:
        try:
            insertedId = IDMapping[key]
            productIDs = masterDict[key]
            for currid in productIDs:
                try:
                    cursor.execute("UPDATE tablets SET tabletMapping=%d WHERE ID=%d" % (insertedId, currid))
                except:
                    print "error while inserting into tablets"
                    continue
        except:
            print "wrong key"
            continue
conn.commit()
conn.close()
print len(laptopMaster)
count = 0
for i in laptopMaster:
    list = laptopMaster[i]
    if (len(list) > 2):
        count +=1

print count

with open('TabletsMaster.csv', 'wb') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in laptopMaster.items():
       writer.writerow([key, value])