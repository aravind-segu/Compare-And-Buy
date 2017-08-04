import csv

import pandas as pd
from fuzzywuzzy import fuzz

bestBuy = pd.read_csv("./BestBuy/BestBuy.csv")
print bestBuy.columns.values
print
amazon = pd.read_csv("./Amazon/AmazonTablet.csv")
print amazon.columns.values
print amazon.head()
print
newEgg = pd.read_csv("newEgg/newEggModel.csv")
print newEgg.columns.values
print
source = pd.read_csv("./Source/SourceTablets.csv")
print source.columns.values
print
flipkart = pd.read_csv("./Flipkart/FlipkartTablets.csv")
print flipkart.columns.values
print
overStock = pd.read_csv("./OverStock/OverStockTablet.csv")
print overStock.columns.values
print
snapDeal = pd.read_csv("./SnapDeal/snapdealTablets.csv")
print snapDeal.columns.values
print

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

brands = []
brands.append("apple")
brands.append("samsung")
brands.append("acer")
brands.append("asus")
brands.append("lg")
brands.append("hp")
brands.append("microsoft")
brands.append("lenovo")
brands.append("indigi")
brands.append("sony")
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
identifyBrand(brands, overStock)
identifyBrand(brands, snapDeal)

def groupbyBrand(d, dataset):
    name = dataset.groupby("Company")
    for brand in brands:
        d["{0}Data".format(brand)] = pd.DataFrame
        try:
            d["{0}Data".format(brand)] = name.get_group(name=brand)
        except KeyError as e:
            continue

dBestBuy = {}
dAmazon = {}
dNewEgg = {}
dSource = {}
dSnapDeal = {}
dFlipkart = {}
dOverStock = {}
groupbyBrand(dBestBuy, bestBuy)
groupbyBrand(dAmazon, amazon)
groupbyBrand(dNewEgg, newEgg)
groupbyBrand(dSource, source)
groupbyBrand(dSnapDeal, snapDeal)
groupbyBrand(dFlipkart, flipkart)
groupbyBrand(dOverStock, overStock)

class productProperties (object):
    productName = None
    productPrice = None
    productModel = None
    def __init__(self, productName, productModel, productPrice):
        self.productName = productName
        self.productModel = productModel
        self.productPrice = productPrice
    def __eq__(self, other):
        return (self.productModel == other.productModel)
    def __hash__(self):
        return hash(self.productName)
amazon = amazon.rename(columns={"model": "ModelNumber"})
db = dBestBuy['appleData']
print db.groupby('ModelNumber').count()

master = {}
x = 0
for dataset in dBestBuy:
    print dataset
    try:
        print len(dataset)
        for i, row in dBestBuy[dataset].iterrows():
            if row['ModelNumber'] in master:
                print "entered Duplicate"
                print row['ModelNumber']
                productDetails = master[row['ModelNumber']]
                productDetails.append("bestBuy")
                productDetails.append(row["ID"])
            else:
                productDetails = []
                productDetails.append("bestBuy")
                productDetails.append(row["ID"])
                master[row['ModelNumber']] = productDetails
    except:
     continue
print amazon.head()
name = amazon.groupby("Model")
amazonPlain = amazon[amazon["Model"] == "none"]
amazonModelNumber = amazon[amazon["Model"] != "none"]
print len(amazon)
print len(amazonPlain)
print len(amazonModelNumber)
for i, row in amazonModelNumber.iterrows():
    if row['Model'].strip() in master:
        print "entered Duplicate"
        print row['Model']
        productDetails = master[row['Model'].strip()]
        productDetails.append("amazon")
        productDetails.append(row["ID"])
    else:
        productDetails = []
        productDetails.append("amazon")
        productDetails.append(row["ID"])
        master[row['Model'].strip()] = productDetails

for i, row in source.iterrows():
    if row['ModelNumber'].strip() in master:
        print "entered Duplicate"
        print row['ModelNumber']
        productDetails = master[row['ModelNumber'].strip()]
        productDetails.append("source")
        productDetails.append(row["ID"])
    else:
        productDetails = []
        productDetails.append("source")
        productDetails.append(row["ID"])
        master[row['ModelNumber'].strip()] = productDetails

overStockPlain = overStock[overStock["ModelNumber"] == "none"]
overStockModelNumber = overStock[overStock["ModelNumber"] != "none"]
print len(overStock)
print len(overStockPlain)
for i, row in overStockModelNumber.iterrows():
    if row['ModelNumber'] in master:
        print "entered Duplicate"
        print row['ModelNumber']
        productDetails = master[row['ModelNumber']]
        productDetails.append("overStock")
        productDetails.append(row["ID"])
    else:
        productDetails = []
        productDetails.append("overStock")
        productDetails.append(row["ID"])
        master[row['ModelNumber']] = productDetails

flipkartPlain = flipkart[flipkart["ModelNumber"] == "none"]
flipkartModelNumber = flipkart[flipkart["ModelNumber"] != "none"]
print len(flipkart)
print len(flipkartPlain)
print len(flipkartModelNumber)

for i, row in flipkartModelNumber.iterrows():
    if row['ModelNumber'] in master:
        print "entered Duplicate"
        print row['ModelNumber']
        productDetails = master[row['ModelNumber']]
        productDetails.append("flipkart")
        productDetails.append(row["ID"])
    else:
        productDetails = []
        productDetails.append("flipkart")
        productDetails.append(row["ID"])
        master[row['ModelNumber']] = productDetails

snapDealPlain = snapDeal[snapDeal["ModelNumber"] == "none"]
snapDealModelNumber = snapDeal[snapDeal["ModelNumber"] != "none"]
print len(snapDeal)
print len(snapDealPlain)
print len(snapDealModelNumber)

for i, row in snapDealModelNumber.iterrows():
    if row['ModelNumber'] in master:
        print "entered Duplicate"
        print row['ModelNumber']
        productDetails = master[row['ModelNumber']]
        productDetails.append("snapdeal")
        productDetails.append(row["ID"])
    else:
        productDetails = []
        productDetails.append("snapdeal")
        productDetails.append(row["ID"])
        master[row['ModelNumber']] = productDetails
newEggPlain = newEgg[newEgg["ModelNumber"] == "none"]
newEggModelNumber = newEgg[newEgg["ModelNumber"] != "none"]
print len(newEgg)
print len(newEggPlain)
print len(newEggModelNumber)
for i, row in newEggModelNumber.iterrows():
    if row['ModelNumber'].strip() in master:
        print "entered Duplicate"
        print row['ModelNumber']
        productDetails = master[row['ModelNumber']]
        productDetails.append("newEgg")
        productDetails.append(row["ID"])
    else:
        productDetails = []
        productDetails.append("newEgg")
        productDetails.append(row["ID"])
        master[row['ModelNumber']] = productDetails

print "Amazon: " + str(len(amazonPlain))
print "Flipkart: " + str(len(flipkartPlain))
print "SnapDeal: " + str(len(snapDealPlain))
print "newEgg: " + str(len(newEggPlain))
print "overStock: " + str(len(overStockPlain))
def checkEquality (name1, name2, price1,price2, countSame):
    similarity = fuzz.token_set_ratio(name1, name2)
    if (similarity > 85):
        if (abs(price2 - price1) < 50.0):
            print "Similarity: " + str(similarity) + " " + name1 + " " + name2
            return True
        else:
            return False
    else:
        return False
found = False
count = 0
ids = []

for i, row in newEgg.iterrows():
    for modelNumber in master:
        productDetails = master[modelNumber]
        if (productDetails[0] == "bestBuy"):
            bestBuyId = productDetails[1]
            rowName = bestBuy[bestBuy.ID == bestBuyId].Name.item()
            rowPrice = bestBuy[bestBuy.ID == bestBuyId].Price.item()
            if (checkEquality(rowName, row["Name"], row["Price"], rowPrice,count)):
                print count
                ids.append("Best Buy: " + str(bestBuyId))
                productDetails.append("newEgg")
                productDetails.append(row["ID"])
                found = True
                break
            else:
                continue
        if (productDetails[0] == "amazon"):
            amazonId = productDetails[1]
            rowName = amazon[amazon.ID == amazonId].Name.item()
            rowPrice = amazon[amazon.ID == amazonId].Price.item()
            if (checkEquality(rowName, row["Name"], row["Price"], rowPrice,count)):
                print count
                ids.append("Amazon: " + str(amazonId))
                productDetails.append("newEgg")
                productDetails.append(row["ID"])
                found = True
                break
            else:
                continue
        if (productDetails[0] == "source"):
            sourceId = productDetails[1]
            rowName = source[source.ID == sourceId].Name.item()
            rowPrice = source[source.ID == sourceId].Price.item()
            if (checkEquality(rowName, row["Name"], row["Price"], rowPrice,count)):
                print count
                ids.append("Source: " + str(sourceId))
                productDetails.append("newEgg")
                productDetails.append(row["ID"])
                found = True
                break
            else:
                continue
        if (productDetails[0] == "newEgg"):
            newEggId = productDetails[1]
            rowName = newEgg[newEgg.ID == newEggId].Name.item()
            rowPrice = newEgg[newEgg.ID == newEggId].Price.item()
            if (checkEquality(rowName,row["Name"],rowPrice,row["Price"],count)):
                print count
                ids.append("New Egg: " + str(newEggId))
                productDetails.append("newEgg")
                productDetails.append(row["ID"])
                found = True
                break
            else:
                continue
        if (productDetails[0] == "flipkart"):
            flipkartId = productDetails[1]
            rowName = flipkart[flipkart.ID == flipkartId].Name.item()
            rowPrice = flipkart[flipkart.ID == flipkartId].Price.item()
            if (checkEquality(rowName,row["Name"], row["Price"],rowPrice,count)):
                print count
                ids.append("Flipkart: " + str(flipkartId))
                productDetails.append("newEgg")
                productDetails.append(row["ID"])
                found = True
                break
            else:
                continue
        if (productDetails[0] == "snapdeal"):
            snapdealId = productDetails[1]
            rowName = snapDeal[snapDeal.ID == snapdealId].Name.item()
            rowPrice = snapDeal[snapDeal.ID == snapdealId].Price.item()
            if (checkEquality(rowName, row["Name"], row["Price"], rowPrice,count)):
                print count
                ids.append("Snapdeal: " + str(snapdealId))
                productDetails.append("newEgg")
                productDetails.append(row["ID"])
                found = True
                break
            else:
                continue
        if (productDetails[0] == "overStock"):
            overStockId = productDetails[1]
            rowName = overStock[overStock.ID == overStockId].Name.item()
            rowPrice = overStock[overStock.ID == overStockId].Price.item()
            if (checkEquality(rowName, row["Name"], row["Price"], rowPrice,count)):
                print count
                ids.append("OverStock: " + str(overStockId))
                productDetails.append("newEgg")
                productDetails.append(row["ID"])
                found = True
                break
            else:
                continue
    if (found == False):
        print count
        print "Entered"
        productDetails = []
        productDetails.append("newEgg")
        productDetails.append(row["ID"])
        master[row["Name"]] = productDetails
    print len(master)
    found = False
    count += 1

for i, row in amazonPlain.iterrows():
    for modelNumber in master:
        productDetails = master[modelNumber]
        if (productDetails[0] == "bestBuy"):
            bestBuyId = productDetails[1]
            rowName = bestBuy[bestBuy.ID == bestBuyId].Name.item()
            rowPrice = bestBuy[bestBuy.ID == bestBuyId].Price.item()
            if (checkEquality(rowName, row["Name"], row["Price"], rowPrice,count)):
                print count
                ids.append("Best Buy: " + str(bestBuyId))
                productDetails.append("amazon")
                productDetails.append(row["ID"])
                found = True
                break
            else:
                continue
        if (productDetails[0] == "amazon"):
            amazonId = productDetails[1]
            rowName = amazon[amazon.ID == amazonId].Name.item()
            rowPrice = amazon[amazon.ID == amazonId].Price.item()
            if (checkEquality(rowName, row["Name"], row["Price"], rowPrice,count)):
                print count
                ids.append("Amazon: " + str(amazonId))
                productDetails.append("amazon")
                productDetails.append(row["ID"])
                found = True
                break
            else:
                continue
        if (productDetails[0] == "source"):
            sourceId = productDetails[1]
            rowName = source[source.ID == sourceId].Name.item()
            rowPrice = source[source.ID == sourceId].Price.item()
            if (checkEquality(rowName, row["Name"], row["Price"], rowPrice,count)):
                print count
                ids.append("Source: " + str(sourceId))
                productDetails.append("amazon")
                productDetails.append(row["ID"])
                found = True
                break
            else:
                continue
        if (productDetails[0] == "newEgg"):
            newEggId = productDetails[1]
            rowName = newEgg[newEgg.ID == newEggId].Name.item()
            rowPrice = newEgg[newEgg.ID == newEggId].Price.item()
            if (checkEquality(rowName,row["Name"],rowPrice,row["Price"],count)):
                print count
                ids.append("New Egg: " + str(newEggId))
                productDetails.append("amazon")
                productDetails.append(row["ID"])
                found = True
                break
            else:
                continue
        if (productDetails[0] == "flipkart"):
            flipkartId = productDetails[1]
            rowName = flipkart[flipkart.ID == flipkartId].Name.item()
            rowPrice = flipkart[flipkart.ID == flipkartId].Price.item()
            if (checkEquality(rowName,row["Name"], row["Price"],rowPrice,count)):
                print count
                ids.append("Flipkart: " + str(flipkartId))
                productDetails.append("amazon")
                productDetails.append(row["ID"])
                found = True
                break
            else:
                continue
        if (productDetails[0] == "snapdeal"):
            snapdealId = productDetails[1]
            rowName = snapDeal[snapDeal.ID == snapdealId].Name.item()
            rowPrice = snapDeal[snapDeal.ID == snapdealId].Price.item()
            if (checkEquality(rowName, row["Name"], row["Price"], rowPrice,count)):
                print count
                ids.append("Snapdeal: " + str(snapdealId))
                productDetails.append("amazon")
                productDetails.append(row["ID"])
                found = True
                break
            else:
                continue
        if (productDetails[0] == "overStock"):
            overStockId = productDetails[1]
            rowName = overStock[overStock.ID == overStockId].Name.item()
            rowPrice = overStock[overStock.ID == overStockId].Price.item()
            if (checkEquality(rowName, row["Name"], row["Price"], rowPrice,count)):
                print count
                ids.append("OverStock: " + str(overStockId))
                productDetails.append("amazon")
                productDetails.append(row["ID"])
                found = True
                break
            else:
                continue
    if (found == False):
        print count
        print "Entered"
        productDetails = []
        productDetails.append("amazon")
        productDetails.append(row["ID"])
        master[row["Name"]] = productDetails
    print len(master)
    found = False
    count += 1

for i, row in overStockPlain.iterrows():
    for modelNumber in master:
        productDetails = master[modelNumber]
        if (productDetails[0] == "bestBuy"):
            bestBuyId = productDetails[1]
            rowName = bestBuy[bestBuy.ID == bestBuyId].Name.item()
            rowPrice = bestBuy[bestBuy.ID == bestBuyId].Price.item()
            if (checkEquality(rowName, row["Name"], row["Price"], rowPrice,count)):
                print count
                ids.append("Best Buy: " + str(bestBuyId))
                productDetails.append("overstock")
                productDetails.append(row["ID"])
                found = True
                break
            else:
                continue
        if (productDetails[0] == "amazon"):
            amazonId = productDetails[1]
            rowName = amazon[amazon.ID == amazonId].Name.item()
            rowPrice = amazon[amazon.ID == amazonId].Price.item()
            if (checkEquality(rowName, row["Name"], row["Price"], rowPrice,count)):
                print count
                ids.append("Amazon: " + str(amazonId))
                productDetails.append("overstock")
                productDetails.append(row["ID"])
                found = True
                break
            else:
                continue
        if (productDetails[0] == "source"):
            sourceId = productDetails[1]
            rowName = source[source.ID == sourceId].Name.item()
            rowPrice = source[source.ID == sourceId].Price.item()
            if (checkEquality(rowName, row["Name"], row["Price"], rowPrice,count)):
                print count
                ids.append("Source: " + str(sourceId))
                productDetails.append("overstock")
                productDetails.append(row["ID"])
                found = True
                break
            else:
                continue
        if (productDetails[0] == "newEgg"):
            newEggId = productDetails[1]
            rowName = newEgg[newEgg.ID == newEggId].Name.item()
            rowPrice = newEgg[newEgg.ID == newEggId].Price.item()
            if (checkEquality(rowName,row["Name"],rowPrice,row["Price"],count)):
                print count
                ids.append("New Egg: " + str(newEggId))
                productDetails.append("overstock")
                productDetails.append(row["ID"])
                found = True
                break
            else:
                continue
        if (productDetails[0] == "flipkart"):
            flipkartId = productDetails[1]
            rowName = flipkart[flipkart.ID == flipkartId].Name.item()
            rowPrice = flipkart[flipkart.ID == flipkartId].Price.item()
            if (checkEquality(rowName,row["Name"], row["Price"],rowPrice,count)):
                print count
                ids.append("Flipkart: " + str(flipkartId))
                productDetails.append("overstock")
                productDetails.append(row["ID"])
                found = True
                break
            else:
                continue
        if (productDetails[0] == "snapdeal"):
            snapdealId = productDetails[1]
            rowName = snapDeal[snapDeal.ID == snapdealId].Name.item()
            rowPrice = snapDeal[snapDeal.ID == snapdealId].Price.item()
            if (checkEquality(rowName, row["Name"], row["Price"], rowPrice,count)):
                print count
                ids.append("Snapdeal: " + str(snapdealId))
                productDetails.append("overstock")
                productDetails.append(row["ID"])
                found = True
                break
            else:
                continue
        if (productDetails[0] == "overStock"):
            overStockId = productDetails[1]
            rowName = overStock[overStock.ID == overStockId].Name.item()
            rowPrice = overStock[overStock.ID == overStockId].Price.item()
            if (checkEquality(rowName, row["Name"], row["Price"], rowPrice,count)):
                print count
                ids.append("OverStock: " + str(overStockId))
                productDetails.append("overstock")
                productDetails.append(row["ID"])
                found = True
                break
            else:
                continue
    if (found == False):
        print count
        print "Entered"
        productDetails = []
        productDetails.append("overstock")
        productDetails.append(row["ID"])
        master[row["Name"]] = productDetails
    print len(master)
    found = False
    count += 1

for i, row in flipkartPlain.iterrows():
    for modelNumber in master:
        productDetails = master[modelNumber]
        if (productDetails[0] == "bestBuy"):
            bestBuyId = productDetails[1]
            rowName = bestBuy[bestBuy.ID == bestBuyId].Name.item()
            rowPrice = bestBuy[bestBuy.ID == bestBuyId].Price.item()
            if (checkEquality(rowName, row["Name"], row["Price"], rowPrice,count)):
                print count
                ids.append("Best Buy: " + str(bestBuyId))
                productDetails.append("flipkart")
                productDetails.append(row["ID"])
                found = True
                break
            else:
                continue
        if (productDetails[0] == "amazon"):
            amazonId = productDetails[1]
            rowName = amazon[amazon.ID == amazonId].Name.item()
            rowPrice = amazon[amazon.ID == amazonId].Price.item()
            if (checkEquality(rowName, row["Name"], row["Price"], rowPrice,count)):
                print count
                ids.append("Amazon: " + str(amazonId))
                productDetails.append("flipkart")
                productDetails.append(row["ID"])
                found = True
                break
            else:
                continue
        if (productDetails[0] == "source"):
            sourceId = productDetails[1]
            rowName = source[source.ID == sourceId].Name.item()
            rowPrice = source[source.ID == sourceId].Price.item()
            if (checkEquality(rowName, row["Name"], row["Price"], rowPrice,count)):
                print count
                ids.append("Source: " + str(sourceId))
                productDetails.append("flipkart")
                productDetails.append(row["ID"])
                found = True
                break
            else:
                continue
        if (productDetails[0] == "newEgg"):
            newEggId = productDetails[1]
            rowName = newEgg[newEgg.ID == newEggId].Name.item()
            rowPrice = newEgg[newEgg.ID == newEggId].Price.item()
            if (checkEquality(rowName,row["Name"],rowPrice,row["Price"],count)):
                print count
                ids.append("New Egg: " + str(newEggId))
                productDetails.append("flipkart")
                productDetails.append(row["ID"])
                found = True
                break
            else:
                continue
        if (productDetails[0] == "flipkart"):
            flipkartId = productDetails[1]
            rowName = flipkart[flipkart.ID == flipkartId].Name.item()
            rowPrice = flipkart[flipkart.ID == flipkartId].Price.item()
            if (checkEquality(rowName,row["Name"], row["Price"],rowPrice,count)):
                print count
                ids.append("Flipkart: " + str(flipkartId))
                productDetails.append("flipkart")
                productDetails.append(row["ID"])
                found = True
                break
            else:
                continue
        if (productDetails[0] == "snapdeal"):
            snapdealId = productDetails[1]
            rowName = snapDeal[snapDeal.ID == snapdealId].Name.item()
            rowPrice = snapDeal[snapDeal.ID == snapdealId].Price.item()
            if (checkEquality(rowName, row["Name"], row["Price"], rowPrice,count)):
                print count
                ids.append("Snapdeal: " + str(snapdealId))
                productDetails.append("flipkart")
                productDetails.append(row["ID"])
                found = True
                break
            else:
                continue
        if (productDetails[0] == "overStock"):
            overStockId = productDetails[1]
            rowName = overStock[overStock.ID == overStockId].Name.item()
            rowPrice = overStock[overStock.ID == overStockId].Price.item()
            if (checkEquality(rowName, row["Name"], row["Price"], rowPrice,count)):
                print count
                ids.append("OverStock: " + str(overStockId))
                productDetails.append("flipkart")
                productDetails.append(row["ID"])
                found = True
                break
            else:
                continue
    if (found == False):
        print count
        print "Entered"
        productDetails = []
        productDetails.append("flipkart")
        productDetails.append(row["ID"])
        master[row["Name"]] = productDetails
    print len(master)
    found = False
    count += 1

for i, row in snapDealPlain.iterrows():
    for modelNumber in master:
        productDetails = master[modelNumber]
        if (productDetails[0] == "bestBuy"):
            bestBuyId = productDetails[1]
            rowName = bestBuy[bestBuy.ID == bestBuyId].Name.item()
            rowPrice = bestBuy[bestBuy.ID == bestBuyId].Price.item()
            if (checkEquality(rowName, row["Name"], row["Price"], rowPrice,count)):
                print count
                ids.append("Best Buy: " + str(bestBuyId))
                productDetails.append("snapdeal")
                productDetails.append(row["ID"])
                found = True
                break
            else:
                continue
        if (productDetails[0] == "amazon"):
            amazonId = productDetails[1]
            rowName = amazon[amazon.ID == amazonId].Name.item()
            rowPrice = amazon[amazon.ID == amazonId].Price.item()
            if (checkEquality(rowName, row["Name"], row["Price"], rowPrice,count)):
                print count
                ids.append("Amazon: " + str(amazonId))
                productDetails.append("snapdeal")
                productDetails.append(row["ID"])
                found = True
                break
            else:
                continue
        if (productDetails[0] == "source"):
            sourceId = productDetails[1]
            rowName = source[source.ID == sourceId].Name.item()
            rowPrice = source[source.ID == sourceId].Price.item()
            if (checkEquality(rowName, row["Name"], row["Price"], rowPrice,count)):
                print count
                ids.append("Source: " + str(sourceId))
                productDetails.append("snapdeal")
                productDetails.append(row["ID"])
                found = True
                break
            else:
                continue
        if (productDetails[0] == "newEgg"):
            newEggId = productDetails[1]
            rowName = newEgg[newEgg.ID == newEggId].Name.item()
            rowPrice = newEgg[newEgg.ID == newEggId].Price.item()
            if (checkEquality(rowName,row["Name"],rowPrice,row["Price"],count)):
                print count
                ids.append("New Egg: " + str(newEggId))
                productDetails.append("snapdeal")
                productDetails.append(row["ID"])
                found = True
                break
            else:
                continue
        if (productDetails[0] == "flipkart"):
            flipkartId = productDetails[1]
            rowName = flipkart[flipkart.ID == flipkartId].Name.item()
            rowPrice = flipkart[flipkart.ID == flipkartId].Price.item()
            if (checkEquality(rowName,row["Name"], row["Price"],rowPrice,count)):
                print count
                ids.append("Flipkart: " + str(flipkartId))
                productDetails.append("snapdeal")
                productDetails.append(row["ID"])
                found = True
                break
            else:
                continue
        if (productDetails[0] == "snapdeal"):
            snapdealId = productDetails[1]
            rowName = snapDeal[snapDeal.ID == snapdealId].Name.item()
            rowPrice = snapDeal[snapDeal.ID == snapdealId].Price.item()
            if (checkEquality(rowName, row["Name"], row["Price"], rowPrice,count)):
                print count
                ids.append("Snapdeal: " + str(snapdealId))
                productDetails.append("snapdeal")
                productDetails.append(row["ID"])
                found = True
                break
            else:
                continue
        if (productDetails[0] == "overStock"):
            overStockId = productDetails[1]
            rowName = overStock[overStock.ID == overStockId].Name.item()
            rowPrice = overStock[overStock.ID == overStockId].Price.item()
            if (checkEquality(rowName, row["Name"], row["Price"], rowPrice,count)):
                print count
                ids.append("OverStock: " + str(overStockId))
                productDetails.append("snapdeal")
                productDetails.append(row["ID"])
                found = True
                break
            else:
                continue
    if (found == False):
        print count
        print "Entered"
        productDetails = []
        productDetails.append("snapdeal")
        productDetails.append(row["ID"])
        master[row["Name"]] = productDetails
    print len(master)
    found = False
    count += 1



print len(master)
count = 0
for i in master:
    list = master[i]
    if (len(list) > 2):
        count +=1

print count

print master["MLMV2LL/A"]
with open('dict4.csv', 'wb') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in master.items():
       writer.writerow([key, value])

