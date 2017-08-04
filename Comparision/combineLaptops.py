import csv
import threading

import pandas as pd
from fuzzywuzzy import fuzz

bestBuy = pd.read_csv("./BestBuy/BestBuyLaptops.csv")
print bestBuy.columns.values
bestBuy["name"] = "bestbuy"
print bestBuy.head()
print bestBuy.shape

amazon = pd.read_csv("./Amazon/AmazonLaptop.csv")
print amazon.columns.values
amazon.columns = ["ID", "Name", "Price", "Link", "Images", "ModelNumber"]
amazon["name"] = "amazon"
print amazon.columns.values
print amazon.shape

newEgg = pd.read_csv("./newEgg/newEggLaptopModel.csv")
print newEgg.columns.values
newEgg["name"] = "newEgg"
print newEgg.shape

flipkart = pd.read_csv("./Flipkart/FlipkartLaptops.csv")
print flipkart.columns.values
flipkart["name"] = "flipkart"
print flipkart.shape

snapDeal = pd.read_csv("./SnapDeal/snapdealLaptops.csv")
print snapDeal.columns.values
snapDeal["name"] = "snapdeal"
print snapDeal.shape

source = pd.read_csv("./Source/SourceLaptops.csv")
print source.columns.values
source["name"] = "source"
print source.shape

staples = pd.read_csv("./Staples/Staples.csv")
print staples.columns.values
staples.columns = ["ID", "Name", "Price", "Link", "ModelNumber", "Image"]
staples["name"] = "staples"
print staples.shape

walmart = pd.read_csv("./Walmart/walmartLaptops.csv")
print walmart.columns.values
walmart["name"] = "walmart"
print walmart.shape

def priceCorrection(dataset):
    newPriceBestBuy= []
    for price in dataset["Price"]:
        aInt = int(filter(str.isdigit, price))
        newPriceBestBuy.append(aInt * 0.01)
    dataset.drop('Price', axis=1, inplace= True)
    dataset.insert(4, "Price", newPriceBestBuy)

priceCorrection(bestBuy)
priceCorrection(amazon)
priceCorrection(source)
priceCorrection(newEgg)
priceCorrection(staples)
priceCorrection(walmart)
combinedDataset = [bestBuy, amazon, source, newEgg, staples, walmart, flipkart, snapDeal]
dollars = []
for price in snapDeal["Price"]:
    dollars.append(round(price * 0.019,2))
snapDeal.drop('Price', axis=1, inplace= True)
snapDeal.insert(4, "Price", dollars)

dollars = []
for price in flipkart["Price"]:
    aInt = int(filter(str.isdigit, price))
    dollars.append(round(aInt * 0.019,2))
flipkart.drop('Price', axis=1, inplace= True)
flipkart.insert(4, "Price", dollars)

print flipkart.head()

brands = []
brands.append("acer")
brands.append("asus")
brands.append("dell")
brands.append("hp")
brands.append("lenovo")
brands.append("microsoft")
brands.append("toshiba")
brands.append("apple")
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
identifyBrand(brands, source)
identifyBrand(brands, flipkart)
identifyBrand(brands, staples)
identifyBrand(brands, walmart)
identifyBrand(brands, snapDeal)


def groupByBrand(combinedDataset , d, companyNames, brandName):
    i = 0
    for dataset in combinedDataset:
        name = dataset.groupby("Company")
        d["{0}Data".format(companyNames[i])] = pd.DataFrame
        try:
            d["{0}Data".format(companyNames[i])] = name.get_group(name = brandName)
            i+=1
        except KeyError as e:
            i+=1
            continue

dAcer = {}
dAsus = {}
dDell = {}
dHp = {}
dLenovo = {}
dMicrosoft = {}
dToshiba = {}
dApple = {}
dOther = {}
combinedBrandDataset = [dAcer, dAsus, dDell, dHp, dLenovo, dMicrosoft, dToshiba, dApple, dOther]
companyNames = []
companyNames.append("bestbuy")
companyNames.append("amazon")
companyNames.append("source")
companyNames.append("newEgg")
companyNames.append("staples")
companyNames.append("walmart")
companyNames.append("flipkart")
companyNames.append("snapDeal")

groupByBrand(combinedDataset, dAcer, companyNames, "acer")
groupByBrand(combinedDataset, dAsus, companyNames, "asus")
groupByBrand(combinedDataset, dDell, companyNames, "dell")
groupByBrand(combinedDataset, dHp, companyNames, "hp")
groupByBrand(combinedDataset, dLenovo, companyNames, "lenovo")
groupByBrand(combinedDataset, dMicrosoft, companyNames, "microsoft")
groupByBrand(combinedDataset, dToshiba, companyNames, "toshiba")
groupByBrand(combinedDataset, dApple, companyNames, "apple")
groupByBrand(combinedDataset, dOther, companyNames, "other")
print "starting"
for d in dAcer:
    print d
    print dAcer[d].shape


threads = []
def checkEquality (name1, name2, price1,price2, countSame):
    similarity = fuzz.token_set_ratio(name1, name2)
    if (similarity > 85):
        if (abs(price2 - price1) < 50.0):
            print str(countSame) + " Similarity: " + str(similarity) + " " + name1 + " " + name2
            return True
        else:
            return False
    else:
        return False

def comparePlain (combinedPlain, master):
    count = 0
    found = False
    for dataset in combinedPlain:
        for i, row in dataset.iterrows():
            for modelNumber in master.keys():
                productDetails = master[modelNumber]
                if (productDetails[0] == "bestbuy"):
                    bestBuyId = productDetails[1]
                    rowName = bestBuy[bestBuy.ID == bestBuyId].Name.item()
                    rowPrice = bestBuy[bestBuy.ID == bestBuyId].Price.item()
                    if (checkEquality(rowName, row["Name"], row["Price"], rowPrice, count)):
                        productDetails.append(row["name"])
                        productDetails.append(row["ID"])
                        found = True
                        break
                    else:
                        continue
                if (productDetails[0] == "amazon"):
                    bestBuyId = productDetails[1]
                    rowName = amazon[amazon.ID == bestBuyId].Name.item()
                    rowPrice = amazon[amazon.ID == bestBuyId].Price.item()
                    if (checkEquality(rowName, row["Name"], row["Price"], rowPrice, count)):
                        productDetails.append(row["name"])
                        productDetails.append(row["ID"])
                        found = True
                        break
                    else:
                        continue
                if (productDetails[0] == "newEgg"):
                    bestBuyId = productDetails[1]
                    rowName = newEgg[newEgg.ID == bestBuyId].Name.item()
                    rowPrice = newEgg[newEgg.ID == bestBuyId].Price.item()
                    if (checkEquality(rowName, row["Name"], row["Price"], rowPrice, count)):
                        productDetails.append(row["name"])
                        productDetails.append(row["ID"])
                        found = True
                        break
                    else:
                        continue
                if(productDetails[0] == "flipkart"):
                    bestBuyId = productDetails[1]
                    rowName = flipkart[flipkart.ID == bestBuyId].Name.item()
                    rowPrice = flipkart[flipkart.ID == bestBuyId].Price.item()
                    if (checkEquality(rowName, row["Name"], row["Price"], rowPrice, count)):
                        productDetails.append(row["name"])
                        productDetails.append(row["ID"])
                        found = True
                        break
                    else:
                        continue
                if (productDetails[0] == "snapdeal"):
                    bestBuyId = productDetails[1]
                    rowName = snapDeal[snapDeal.ID == bestBuyId].Name.item()
                    rowPrice = snapDeal[snapDeal.ID == bestBuyId].Price.item()
                    if (checkEquality(rowName, row["Name"], row["Price"], rowPrice, count)):
                        productDetails.append(row["name"])
                        productDetails.append(row["ID"])
                        found = True
                        break
                    else:
                        continue
                if (productDetails[0] == "source"):
                    bestBuyId = productDetails[1]
                    rowName = source[source.ID == bestBuyId].Name.item()
                    rowPrice = source[source.ID == bestBuyId].Price.item()
                    if (checkEquality(rowName, row["Name"], row["Price"], rowPrice, count)):
                        productDetails.append(row["name"])
                        productDetails.append(row["ID"])
                        found = True
                        break
                    else:
                        continue
                if (productDetails[0] == "staples"):
                    bestBuyId = productDetails[1]
                    rowName = staples[staples.ID == bestBuyId].Name.item()
                    rowPrice = staples[staples.ID == bestBuyId].Price.item()
                    if (checkEquality(rowName, row["Name"], row["Price"], rowPrice, count)):
                        productDetails.append(row["name"])
                        productDetails.append(row["ID"])
                        found = True
                        break
                    else:
                        continue
                if (productDetails[0] == "walmart"):
                    bestBuyId = productDetails[1]
                    rowName = walmart[walmart.ID == bestBuyId].Name.item()
                    rowPrice = walmart[walmart.ID == bestBuyId].Price.item()
                    if (checkEquality(rowName, row["Name"], row["Price"], rowPrice, count)):
                        productDetails.append(row["name"])
                        productDetails.append(row["ID"])
                        found = True
                        break
                    else:
                        continue
            if (found == False):
                print count
                print "Entered"
                productDetails = []
                productDetails.append(row["name"])
                productDetails.append(row["ID"])
                master[row["Name"]] = productDetails
            found = False
            count += 1
combinedMaster = []
for dBrand in combinedBrandDataset:
    combinedPlain = []
    master = {}
    for data in dBrand:
       try:
           d = dBrand[data]
           dPlain = d[d["ModelNumber"] == "none"]
           dModelNumber = d[d["ModelNumber"] != "none"]
           combinedPlain.append(dPlain)
           for i, row in dModelNumber.iterrows():
               if row['ModelNumber'].strip() in master:
                   productDetails = master[row['ModelNumber'].strip()]
                   productDetails.append(row["name"])
                   productDetails.append(row["ID"])
               else:
                   productDetails = []
                   productDetails.append(row["name"])
                   productDetails.append(row["ID"])
                   master[row["ModelNumber"].strip()] = productDetails
       except Exception as e:
           continue
    combinedMaster.append(master)
    print len(master)
    t1 = threading.Thread(target=comparePlain, args=(combinedPlain,master,))
    t1.start()
    threads.append(t1)


for thread in threads:
    thread.join()

laptopMaster = {}
for masterDict in combinedMaster:
    laptopMaster.update(masterDict)
print len(laptopMaster)
count = 0
for i in laptopMaster:
    list = laptopMaster[i]
    if (len(list) > 2):
        count +=1

print count

with open('dictLaptops.csv', 'wb') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in laptopMaster.items():
       writer.writerow([key, value])