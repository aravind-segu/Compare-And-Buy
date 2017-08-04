import pandas as pd

newEgg = pd.read_csv("./newEggLaptops.csv")
print newEgg.columns.values
print len (newEgg)
newEgg = newEgg.drop_duplicates(subset='Link')
print len(newEgg)
newEgg.to_csv("newEggLaptops.csv",index=False, encoding='utf-8')