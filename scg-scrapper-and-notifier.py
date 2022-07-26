from selenium import webdriver
import re
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import subprocess
from tqdm import tqdm

chromeoptions=Options()
#chromeoptions.add_argument('--headless')
#chromeoptions.add_argument('--silent')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chromeoptions)
dateandtime = datetime.datetime.now()
products=[]
prices=[]
links=[]
conditions=[]
stocks=[]
sets=[]
maxpages=20
https://starcitygames.com/search/?sort=pricedesc&hawksearchable=search_includetext%3A%20%22default%22&instockonly=Yes&language=Japanese&mpp=96&pg=
url=''
print('Scrapping SCG Japanese stock')

for j in tqdm (range (1, maxpages), desc='Scrapping...'):
    finalurl=url + str(j)
    driver.get(finalurl)
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')

    for variants in soup.find_all('div', class_='hawk-results-item'):
        print(variants)
        name=variants.find('div', re.compile('_item_lnk2'))
        set=variants.find('div', re.compile('item_setLink'))
        link=set['href']
        condition=variants.find('div', class_='hawk-results-item__options-table-cell hawk-results-item__options-table-cell--name childCondition')
        price=variants.find('div', class_='hawk-results-item__options-table-cell hawk-results-item__options-table-cell--price childAttributes')
        stock=variants.find('div', class_='hawk-results-item__options-table-cell hawk-results-item__options-table-cell--qty childAttributes')
        print(name)
        print(set)
        print(link)
        print(condition)
        print(price)
        print(stock)
        conditions+=[condition]
        products+=[name]
        prices+=[price]
        sets+=[set]
        stocks+=[stock]
        links+=[link]

#olddf = pd.read_csv('mtgpirulo-japanese-stock.csv')
#csvfilename = 'mtgpirulo-new-results' + dateandtime.strftime('%y-%m-%d %H:%M') + '.csv'
newdf = pd.DataFrame({'Product':products, 'Price':prices, 'Condition':conditions, 'Set':sets, 'Stock':stocks, 'Link':links})
newdf.to_csv('scg-japanese-stock.csv')
#newdf=pd.read_csv(csvfilename)

#mergeddf.to_csv('merged' + dateandtime.strftime('%y-%m-%d %H:%M') + '.csv')

#subprocess.call(['open', 'merged.csv'])
#if df.empty==False:
#    subprocess.call(['notify', '-bulk', '-i', excelfilename])