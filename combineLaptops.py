import csv
import threading

import pandas as pd
from fuzzywuzzy import fuzz
import pymysql


conn = pymysql.connect(host='localhost', user='root', db='productdata')
conn.set_charset('utf8')
cursor = conn.cursor()
sql = 'SELECT * from `laptops`;'
cursor.execute(sql)
countrow = cursor.execute(sql)
print(countrow)

# The combined table of laptop is extracted and placed into a pandas dataframe
combinedData = pd.read_sql("SELECT * FROM laptops", con= conn)

# Each product is sorted by vendor and stored into appropriate dataframe
bestBuy = pd.read_sql("SELECT * FROM laptops WHERE VENDOR='bestbuy'", con= conn)


amazon = pd.read_sql("SELECT * FROM laptops WHERE VENDOR='amazon'", con= conn)


newEgg = pd.read_sql("SELECT * FROM laptops WHERE VENDOR='newegg'", con= conn)


flipkart = pd.read_sql("SELECT * FROM laptops WHERE VENDOR='flipkart'", con= conn)


source = pd.read_sql("SELECT * FROM laptops WHERE VENDOR='source'", con= conn)


staples = pd.read_sql("SELECT * FROM laptops WHERE VENDOR='staples'", con= conn)


walmart = pd.read_sql("SELECT * FROM laptops WHERE VENDOR='walmart'", con= conn)


# The price correction method removes any string literals in the price such as '$' ',' and outputs only the price
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
priceCorrection(source)
priceCorrection(newEgg)
priceCorrection(staples)
priceCorrection(walmart)
dollars = []

dollars = []
# The price of the Indian items is converted to Canadian Dollars
for price in flipkart["Price"]:
    aInt = int(filter(str.isdigit, price))
    dollars.append(round(aInt * 0.019,2))
flipkart.drop('Price', axis=1, inplace= True)
flipkart.insert(4, "Price", dollars)

print flipkart.head()
# All datasets are combined into a master dataframe
combinedDataset = [bestBuy, amazon, source, newEgg, staples, walmart, flipkart]

# To make matching easier some of the key brands are identified
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

# The brands are identified and a new column is added to the dataframe
def identifyBrand(brands, dataset):
    company = []
    notFound = True
    counter = 0
    for name in dataset["Name"]:
        counter += 1
        for brand in brands:
            if brand in str(name).lower():
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

# groupByBrand accepts:
    # combined Dataset
        # combination of all the various vendors
    # d
        # the dictionary of the specific Brand
    # companyNames
        # A list containing all the vendor Names
    # brandName
        # The current brandName to group
def groupByBrand(combinedDataset , d, companyNames, brandName):
    i = 0
    # For each dataset in the combined dataset
    # The dataset is grouped by the Company
    # A dynamic variable is set and used as the key for the dictionary to store the dataframe
        #bestBuyData or amazonData etc
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

# Dictionaries are Initialized to hold each of the dataframes
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

groupByBrand(combinedDataset, dAcer, companyNames, "acer")
groupByBrand(combinedDataset, dAsus, companyNames, "asus")
groupByBrand(combinedDataset, dDell, companyNames, "dell")
groupByBrand(combinedDataset, dHp, companyNames, "hp")
groupByBrand(combinedDataset, dLenovo, companyNames, "lenovo")
groupByBrand(combinedDataset, dMicrosoft, companyNames, "microsoft")
groupByBrand(combinedDataset, dToshiba, companyNames, "toshiba")
groupByBrand(combinedDataset, dApple, companyNames, "apple")
groupByBrand(combinedDataset, dOther, companyNames, "other")

#An array is initialized to hold all the threads
threads = []
# The check equality checks the equality of two products utilizing an external library called fuzzy wuzzy
    # A similarity percentage is extracted
    # Prices are adjusted
    # If the similarity is greater than 85 and the price difference is less than 250 it is declared as a match
def checkEquality (name1, name2, price1,price2, countSame,vendor):
    similarity = fuzz.token_set_ratio(name1, name2)
    if (vendor != "flipkart"):
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
    if (similarity > 85):
        if (abs(modPrice - price1) < 250.0):
            return True
        else:
            return False
    else:
        return False

# A list to hold all the masters
combinedMaster = []

# The comparePlain is iterated through
    # The name of the product in the master is extracted
        # The product is checked with the current product for equality
            # If match is found then product is appended to the ID
            # Else process repeats
def comparePlain (combinedPlain, master):
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
    combinedMaster.append(master)

# Each brand is iterated though
    #  A master dictionary is initialized to hold all the resulting combination of products
        # Key: Model Number or Name
        # Value: List of ID's
    #  Each dataset from each vendor is taken from the dBrand dictionary
        # The dataset is broken into two, one without modelNumbers and one with Model Numbers
        # The modelNumber dataframe is iterated through
            # If model number exists in the master its appended to the ID list
            # Else a new key is made and stored
    #  A new thread is started on the comparePlain method passing in the plain dataframe and the master
for dBrand in combinedBrandDataset:
    combinedPlain = []
    master = {}
    for data in dBrand:
           d = dBrand[data]
           dPlain = d[d["ModelNumber"] == "none"]
           dModelNumber = d[d["ModelNumber"] != "none"]
           combinedPlain.append(dPlain)
           for i, row in dModelNumber.iterrows():
               if row['ModelNumber'].strip() in master:
                   productDetails = master[row['ModelNumber'].strip()]
                   productDetails.append(row["ID"])
               else:
                   productDetails = []
                   productDetails.append(row["ID"])
                   master[row["ModelNumber"].strip()] = productDetails
    t1 = threading.Thread(target=comparePlain, args=(combinedPlain,master))
    t1.start()
    threads.append(t1)


# Program waits for all threads to finish execution
for thread in threads:
    thread.join()

laptopMaster = {}
# For each master Diction in the combined Master
    # If more than one product is matched then the rating is set as 2
    # The data is inserted into the laptopCombination Database
for masterDict in combinedMaster:
    IDMapping = {}
    for key in masterDict:
        productIDs = masterDict[key]
        rating = 2
        if (len(productIDs) > 2):
            rating = 1
        try:
            cursor.execute(
                "INSERT into laptopcombination(Name,Rating) VALUES ('%s', '%s')" % \
                (key, rating))
        except:
            print "error while inserting into laptopsCombo"
            continue
        IDMapping[key] = cursor.lastrowid
    conn.commit()
# For all the IDs in the master dictionary
    # The Foreign key is set to the updated value
    for key in masterDict:
        try:
            insertedId = IDMapping[key]
            productIDs = masterDict[key]
            for currid in productIDs:
                try:
                    cursor.execute("UPDATE laptops SET laptopMapping=%d WHERE ID=%d" % (insertedId, currid))
                except:
                    print "error while inserting into laptops"
                    continue
        except:
            print "wrong key"
            continue
conn.commit()
conn.close()
# print len(laptopMaster)
# count = 0
# for i in laptopMaster:
#     list = laptopMaster[i]
#     if (len(list) > 2):
#         count +=1
#
# print count
#
# with open('dictLaptops.csv', 'wb') as csv_file:
#     writer = csv.writer(csv_file)
#     for key, value in laptopMaster.items():
#        writer.writerow([key, value])