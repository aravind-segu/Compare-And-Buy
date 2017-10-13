import requests

url = 'http://www.ows.newegg.com/Stores.egg'
r = requests.get(url)
electronics = requests.get(url + "/Categories/13")
print electronics
