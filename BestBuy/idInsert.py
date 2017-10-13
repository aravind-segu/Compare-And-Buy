import pandas as pd
import sys
import operator
from bs4 import BeautifulSoup
import urllib2

bestBuy = pd.read_csv("./BestBuyCameras.csv")
title = bestBuy["Name"]
bestBuy.insert(0, 'ID', range(0, len(title)))
bestBuy.to_csv("BestBuyCameras.csv",index=False, encoding='utf-8')