import urllib2
from bs4 import BeautifulSoup
import pandas as pd
from difflib import SequenceMatcher
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def similar(a, b):
    return fuzz.token_set_ratio(a,b)
def comparePrice(a, b):
    aInt = int(filter(str.isdigit, a))
    bInt = int(filter(str.isdigit, b))
    return abs(aInt - bInt)
brands = []
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
url = "http://www.bestbuy.ca/en-CA/category/tablets-ipads/30297.aspx?type=product&page=1&pageSize=96"
page = opener.open(url)
soup = BeautifulSoup(page)
all_ul = soup.findAll("ul", {"class":"facet-brandName-list"})
for ul in all_ul:
    for li in ul.findAll("li"):
        brand = li.find("span", {"class": "item"})
        if not brand:
            continue
        else:
            strBand = str(brand.text)
            lower = strBand.lower()
            brands.append(lower)

print brands

bestBuy = pd.read_csv("BestBuy.csv")
print bestBuy.head()
company = []
NotFoundBrand = True

for name in bestBuy['Name']:
    for brand in brands:
        if brand in name.lower():
            company.append(brand)
            NotFoundBrand = False
            break
    if NotFoundBrand:
        print "entered"
        company.append("other")
    NotFoundBrand = True

bestBuy.insert(0, "Company", company)

amazon = pd.read_csv("Information.csv")

company = []
NotFoundBrand = True

for name in amazon['Name']:
    for brand in brands:
        if brand in name.lower():
            company.append(brand)
            NotFoundBrand = False
            break
    if NotFoundBrand:
        company.append("other")
    NotFoundBrand = True

amazon.insert(0, "Company", company)
print amazon.head()

print bestBuy["Company"].value_counts()
print amazon["Company"].value_counts()

hpBestBuy = bestBuy.loc[bestBuy["Company"] == "apple"]
hpAmazon = amazon.loc[amazon["Company"] == "apple"]

rating = []


#print next(hpBestBuy.iterrows())
#print
#print

#for name in hpBestBuy["Name"]:
    #for nameAmazon in hpAmazon["Name"]:
        #rating.append(similar(str(name), str(nameAmazon)))
        #if (similar(str(name), str(nameAmazon) )>= 0.7):

#            print name
 #           print nameAmazon
  #          print
   #         print

matchFound = False

columns = ["bestBuyName", "bestBuyPrice", "bestBuyLink", "amazonName", "amazonPrice", "amazonLink"]
appleDf = pd.DataFrame(columns = columns)

for bestBuyC in range (0, len(hpBestBuy)):
    nextBestBuy = hpBestBuy.iloc[bestBuyC]
    for amazonC in range (0, len(hpAmazon)):
        nextAmazon = hpAmazon.iloc[amazonC]
        if (similar(str(nextAmazon["Name"]), str(nextBestBuy["Name"])) >= 85):

            if (comparePrice(str(nextAmazon["Price"]), str(nextBestBuy["Price"])) < 5000):
                print ("Entered")
                appleDf.loc[len(appleDf) - 1] = [nextBestBuy["Name"], nextBestBuy["Price"], nextBestBuy["Link"], nextAmazon["Name"], nextAmazon["Price"], nextAmazon["Link"]]
                break
#while (True):
#    if matchFound:
#        bestBuyC = bestBuyC + 1
#        nextBestBuy = hpBestBuy.iloc[bestBuyC]
#        matchFound = False
#    if (similar(str(nextAmazon["Name"]), str(nextBestBuy["Name"])) >= 0.75):
#        print ("Entered First IF")
#        if(comparePrice(str(nextAmazon["Price"]), str(nextBestBuy["Price"])) < 50):
#            print nextAmazon["Name"]
#            print nextBestBuy["Name"]
#            matchFound = True
#            print("Original")
#            print(amazonC)
#           amazonC = -1
#            print("New")
#           print(amazonC)
#            appleDf["bestBuyName"] = nextBestBuy["Name"]
#            appleDf["bestBuyPrice"] = nextBestBuy["Price"]
#            appleDf["bestBuyLink"] = nextBestBuy["Link"]
#            appleDf["amazonName"] = nextAmazon["Name"]
#            appleDf["amazonPrice"] = nextAmazon["Price"]
#            appleDf["amazonLink"] = nextAmazon["Link"]
#    amazonC = amazonC + 1
#    print amazonC
#    try:
#        nextAmazon = hpAmazon.iloc[amazonC]
#    except IndexError as e:
#        print ("Entered")
#        print amazonC
 #       break

print appleDf
appleDf.to_csv("Comparision.csv",index=False, encoding='utf-8')
#nextAmazon = next(hpAmazon.iterrows())
#print len(rating)
#print len(hpAmazon)
#hpAmazon.insert(0, "rating", rating)
#print hpAmazon.head()
#print hpAmazon["rating"].value_counts()