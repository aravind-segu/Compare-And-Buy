import pandas as pd
import sys
import operator
from bs4 import BeautifulSoup
import urllib2

bestBuy = pd.read_csv("./BestBuyCameras.csv")
print bestBuy.columns.values
bestBuy["name"] = "bestbuy"
bestBuy.set_index("ID", inplace= True)
print bestBuy.head()

imageNew = []
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
for i, rows in bestBuy.iterrows():
    try:
        print rows["Link"]
        page = opener.open(rows["Link"])
        soup = BeautifulSoup(page)
        imageDiv = soup.find("div", {"data-bby-media-container": "primaryMediaContainer"})
        image = imageDiv.find("img")
        imageNew.append(image.get("src"))
    except:
        print "entered Exception"
        imageNew.append("none")
bestBuy.drop('Images', axis=1, inplace= True)
bestBuy.insert(4, "Images", imageNew)
bestBuy.to_csv("BestBuyCameras.csv",index=False, encoding='utf-8')