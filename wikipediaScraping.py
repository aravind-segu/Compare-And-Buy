import urllib2
from bs4 import BeautifulSoup
import pandas as pd

wiki = "https://en.wikipedia.org/wiki/List_of_state_and_union_territory_capitals_in_India"
page = urllib2.urlopen(wiki)
soup = BeautifulSoup(page)
allLinks = soup.find_all("a")
all_tables = soup.find_all("table")
right_table = soup.find('table', class_='wikitable sortable plainrowheaders')

A=[]
B=[]
C=[]
D=[]
E=[]
F=[]
G=[]
for row in right_table.findAll("tr"):
    cells = row.findAll('td')
    states=row.findAll('th')
    if len(cells)==6:
        A.append(cells[0].find(text=True))
        B.append(states[0].find(text=True))
        C.append(cells[1].find(text=True))
        D.append(cells[2].find(text=True))
        E.append(cells[3].find(text=True))
        F.append(cells[4].find(text=True))
        G.append(cells[5].find(text=True))

df=pd.DataFrame(A,columns=['Number'])
df['State/UT'] = B
df['Admin_Capital'] = C
df['Legislative_Capital'] = D
df['Judiciary_Capital'] = E
df['Year Capital'] = F
df['Former_Capital']=G
print(df)
