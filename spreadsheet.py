import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import http
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json',scope)
client = gspread.authorize(creds)

sheet = client.open('Sheets').sheet1
driver = webdriver.Firefox()

def getSchoolData(link):
    driver.get(link)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    i = soup.find_all(attrs={'class': 'cb-link component--field-formatter field-type-integer ng-star-inserted'})
    ints = []
    for x in i:
        ints.append(x.text)
    da = soup.find_all(attrs={'class':'cb-link component--field-formatter field-type-date ng-star-inserted'})
    dates = []
    for x in da:
        dates.append(x.text)
    de = soup.find_all(attrs={'class':'cb-link component--field-formatter field-type-decimal ng-star-inserted'})
    decs = []
    for x in de:
        decs.append(x.text)
#removing variable nums
    mon = soup.find_all(attrs={'class':'cb-link component--field-formatter field-type-money ng-star-inserted'})
    trend = soup.find(attrs={'id':'section-trending'})
    trendnum = trend.find_all(attrs={'class':'cb-link component--field-formatter field-type-money ng-star-inserted'})
    new = []
    for x in mon[len(trendnum):]:
        new.append(x.text)


    final = [ints[0],ints[1],dates[0],decs[0],decs[1],decs[3],new[1],"ints[33]",new[4],new[5],dates[1]]
    return final

def iterateAdd(list):
    it = 0
    for x in list:
        it+=1
        data = getSchoolData(x)
        data.insert(0,x)
        sheet.insert_row(data,1+it)

list = ['https://www.crunchbase.com/hub/stanford-university-alumni-founded-companies-1f27',
'https://www.crunchbase.com/hub/harvard-university-alumni-founded-companies-1164',
'https://www.crunchbase.com/hub/massachusetts-institute-of-technology-mit-alumni-founded-companies-835c',
'https://www.crunchbase.com/hub/university-of-california-berkeley-alumni-founded-companies-297e',
'https://www.crunchbase.com/hub/cornell-university-alumni-founded-companies-12a0',
'https://www.crunchbase.com/hub/university-of-illinois-at-urbana-champaign-alumni-founded-companies',
'https://www.crunchbase.com/hub/columbia-university-alumni-founded-companies-4b7a',
'https://www.crunchbase.com/hub/carnegie-mellon-university-alumni-founded-companies-23c2',
'https://www.crunchbase.com/hub/university-of-michigan-alumni-founded-companies-5157']

iterateAdd(list)
#  11,12,21,31,32,33, 41, 13, 42,43, 22
# nums [0], [1], [33]
# dates [0],[1]
#decs [0], [1], [3]
#new [1], [4], [5]
    # return [orgs[]]
