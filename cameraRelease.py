import pandas as pd

speakers = pd.read_csv("./cameraMaster.csv", names = ["modelNumber", "idNumber"])
laptopsFull = pd.DataFrame()
bestBuy = pd.read_csv("./BestBuy/BestBuyCameras.csv")
print bestBuy.columns.values
bestBuy["name"] = "bestbuy"
bestBuy.set_index("ID", inplace=True)
print bestBuy.head()
print bestBuy.shape

amazon = pd.read_csv("./Amazon/AmazonCameras.csv")
print amazon.columns.values
amazon.columns = ["ID", "Name", "Price", "Link", "Images", "ModelNumber"]
amazon["name"] = "amazon"
print amazon.columns.values
print amazon.shape

newEgg = pd.read_csv("./newEgg/newEggCameras.csv")
print newEgg.columns.values
newEgg["name"] = "newEgg"
newEgg["ModelNumber"] = "none"
print newEgg.shape

snapDeal = pd.read_csv("./SnapDeal/snapdealCameras.csv")
print snapDeal.columns.values
snapDeal["name"] = "snapdeal"
print snapDeal.shape

source = pd.read_csv("./Source/SourceCameras.csv")
print source.columns.values
source["name"] = "source"
print source.shape

staples = pd.read_csv("./Staples/StaplesCameras.csv")
print staples.columns.values
staples.columns = ["ID", "Image", "ModelNumber", "Name", "Price", "Link"]
staples["name"] = "staples"
# print staples.head
# print staples.shape

walmart = pd.read_csv("./Walmart/walmartCameras.csv")
print walmart.columns.values
walmart["name"] = "walmart"
print walmart.shape

rating = [];
for j,row in speakers.iterrows():
    modelNumber = row[0]
    idNumbers = row[1]
    idNumbers = idNumbers.replace("[", "")
    idNumbers = idNumbers.replace("]", "")
    idNumbers = idNumbers.replace("'", "")
    idNumbers = idNumbers.replace("L", "")
    list = idNumbers.split(",")
    print list
    print len(list)
    i = 0
    ratingDict = {}
    ratingDict['snapdeal'] = 0
    ratingDict['bestbuy'] = 0
    ratingDict['amazon'] = 0
    ratingDict['staples'] = 0
    ratingDict['source'] = 0
    ratingDict['walmart'] = 0
    ratingDict['newEgg'] = 0
    ratingDict['flipkart'] = 0
    while (i < len(list)):
        print list[i]
        if (list[i].strip() == 'snapdeal'):
            ratingDict['snapdeal'] += 1
            i += 1
            row = snapDeal.loc[long(list[i])]
            i += 1
            continue
        if (list[i].strip() == 'bestbuy'):
            ratingDict['bestbuy'] += 1
            i += 1
            row = bestBuy.loc[long(list[i])]
            i += 1
            continue
        if (list[i].strip() == 'amazon'):
            ratingDict['amazon'] += 1
            i += 1
            row = amazon.loc[long(list[i])]
            i += 1
            continue
        if (list[i].strip() == 'newEgg'):
            ratingDict['newEgg'] += 1
            i += 1
            row = newEgg.loc[long(list[i])]
            i += 1
            continue
        if (list[i].strip() == 'source'):
            ratingDict['source'] += 1
            i += 1
            row = source.loc[long(list[i])]
            i += 1
            continue
        if (list[i].strip() == 'staples'):
            ratingDict['staples'] += 1
            i += 1
            row = staples.loc[long(list[i])]
            i += 1
            continue
        if (list[i].strip() == 'walmart'):
            ratingDict['walmart'] += 1
            i += 1
            #row = walmart.loc[long(list[i])]
            i += 1
            continue
        if (list[i].strip() == 'flipkart'):
            ratingDict['flipkart'] += 1
            i += 1
            #row = walmart.loc[long(list[i])]
            i += 1
            continue
    ratingCount = 0
    enteredCount = 0
    foundOthers = False
    for key in ratingDict:
        if (ratingDict[key] >= 1):
            enteredCount += ratingDict[key]
            ratingCount += 1
    if enteredCount > 1:
        if ratingCount == 1:
            rating.append(2)
        else:
            rating.append(3)
    else:
        rating.append(1)
speakers["Rating"] = rating
print speakers["Rating"].value_counts()
print speakers.head
speakers.to_csv("cameraMaster.csv",index=False, encoding='utf-8')