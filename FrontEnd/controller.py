from flask import Flask, render_template, request
from tabletsData import getTablets
from tabletsData import getTabletsPage
from tabletsData import getMaxPage
from phonesData import getPhones
from phonesData import getPhonesPage
from phonesData import getMaxPagePhone
from laptopData import getLaptops
from laptopData import getLaptopsPage
from laptopData import getMaxPageLaptop
from desktopData import getDesktops
from desktopData import getDesktopsPage
from desktopData import getMaxPageDesktop
from speakersData import getSpeakers
from speakersData import getMaxPageSpeaker
from speakersData import getSpeakersPage
from printersData import getPrinters
from printersData import getMaxPagePrinter
from printersData import getPrintersPage
from camerasData import getCameras
from camerasData import getCamerasPage
from camerasData import getMaxPageCamera
from TVsData import getTVs
from TVsData import getMaxPageTV
from TVsData import getTVsPage
from difflib import SequenceMatcher
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def similar(a, b):
    return SequenceMatcher(None, str(a), str(b)).ratio()
app = Flask(__name__)

def searchData(searchTerm, searchList):
    searchTabletList = []
    for tablet in searchList:
        found = False
        for tabletInfo in tablet:
            if similar(tabletInfo["Name"], searchTerm) > 0.75:
                found = True
                break
            if str(searchTerm).lower() in str(tabletInfo["Name"]).lower():
                found = True
                break
        if found:
            searchTabletList.append(tablet)
    return searchTabletList

tabletsList = getTablets()
phonesList = getPhones()
laptopsList = getLaptops()
desktopList = getDesktops()
speakerList = getSpeakers()
printerList = getPrinters()
cameraList = getCameras()
tvsList = getTVs()
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/tablets', defaults={'page': 1})
@app.route('/tablets/page/<int:page>')
def tablets(page):
    maxPage = getMaxPage(tabletsList)
    tabletPage = getTabletsPage(tabletsList, page)
    return render_template('tablets.html', tabletsList = tabletPage, page = page, max = maxPage, type = "tablets")

@app.route('/search',  methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        searchTerm =  request.args.get('searchIn')
        searchList =  request.args.get('searchBtn')
        if (searchList == "tablets"):
            searchTabletList = searchData(searchTerm, tabletsList)
            if (len(searchTabletList) == 0):
                return render_template('notFound.html',type="tablets")
            else:
                return render_template('tablets.html', tabletsList=searchTabletList, page=1, max=5, type="tablets")
        if (searchList == "phones"):
            searchTabletList = searchData(searchTerm, phonesList)
            if (len(searchTabletList) == 0):
                return render_template('notFound.html',type="phones")
            else:
                return render_template('tablets.html', tabletsList=searchTabletList, page=1, max=5, type="phones")
        if (searchList == "laptops"):
            searchTabletList = searchData(searchTerm, laptopsList)
            if (len(searchTabletList) == 0):
                return render_template('notFound.html',type="laptops")
            else:
                return render_template('tablets.html', tabletsList=searchTabletList, page=1, max=5, type="laptops")
        if (searchList == "desktops"):
            searchTabletList = searchData(searchTerm, desktopList)
            if (len(searchTabletList) == 0):
                return render_template('notFound.html',type="desktops")
            else:
                return render_template('tablets.html', tabletsList=searchTabletList, page=1, max=5, type="desktops")
        if (searchList == "speakers"):
            searchTabletList = searchData(searchTerm, speakerList)
            if (len(searchTabletList) == 0):
                return render_template('notFound.html',type="speakers")
            else:
                return render_template('tablets.html', tabletsList=searchTabletList, page=1, max=5, type="speakers")
        if (searchList == "printers"):
            searchTabletList = searchData(searchTerm, printerList)
            if (len(searchTabletList) == 0):
                return render_template('notFound.html',type="printers")
            else:
                return render_template('tablets.html', tabletsList=searchTabletList, page=1, max=5, type="printers")
        if (searchList == "cameras"):
            searchTabletList = searchData(searchTerm, cameraList)
            if (len(searchTabletList) == 0):
                return render_template('notFound.html',type="cameras")
            else:
                return render_template('tablets.html', tabletsList=searchTabletList, page=1, max=5, type="cameras")
        if (searchList == "tvs"):
            searchTabletList = searchData(searchTerm, tvsList)
            if (len(searchTabletList) == 0):
                return render_template('notFound.html',type="tvs")
            else:
                return render_template('tablets.html', tabletsList=searchTabletList, page=1, max=5, type="tvs")

    else:
        return render_template('home.html')


@app.route('/phones', defaults={'page': 1})
@app.route('/phones/page/<int:page>')
def phones(page):
    maxPage = getMaxPagePhone(phonesList)
    tabletPage = getPhonesPage(phonesList, page)
    return render_template('tablets.html', tabletsList = tabletPage, page = page, max = maxPage, type= "phones")

@app.route('/laptops', defaults={'page': 1})
@app.route('/laptops/page/<int:page>')
def laptops(page):
    maxPage = getMaxPageLaptop(laptopsList)
    tabletPage = getLaptopsPage(laptopsList, page)
    return render_template('tablets.html', tabletsList = tabletPage, page = page, max = maxPage, type= "laptops")
@app.route('/desktops', defaults={'page': 1})
@app.route('/desktops/page/<int:page>')
def desktops(page):
    maxPage = getMaxPageDesktop(desktopList)
    tabletPage = getDesktopsPage(desktopList, page)
    return render_template('tablets.html', tabletsList = tabletPage, page = page, max = maxPage, type= "desktops")

@app.route('/speakers', defaults={'page': 1})
@app.route('/speakers/page/<int:page>')
def speakers(page):
    maxPage = getMaxPageSpeaker(speakerList)
    tabletPage = getSpeakersPage(speakerList, page)
    return render_template('tablets.html', tabletsList = tabletPage, page = page, max = maxPage, type= "speakers")

@app.route('/printers', defaults={'page': 1})
@app.route('/printers/page/<int:page>')
def printers(page):
    maxPage = getMaxPagePrinter(printerList)
    tabletPage = getPrintersPage(printerList, page)
    return render_template('tablets.html', tabletsList = tabletPage, page = page, max = maxPage, type= "printers")

@app.route('/cameras', defaults={'page': 1})
@app.route('/cameras/page/<int:page>')
def cameras(page):
    maxPage = getMaxPageCamera(cameraList)
    tabletPage = getCamerasPage(cameraList, page)
    return render_template('tablets.html', tabletsList = tabletPage, page = page, max = maxPage, type= "cameras")

@app.route('/tvs', defaults={'page': 1})
@app.route('/tvs/page/<int:page>')
def tvs(page):
    maxPage = getMaxPageTV(tvsList)
    tabletPage = getTVsPage(tvsList, page)
    return render_template('tablets.html', tabletsList = tabletPage, page = page, max = maxPage, type= "tvs")


if __name__ == '__main__':
    app.run()