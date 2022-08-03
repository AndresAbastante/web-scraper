from numpy import true_divide
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
chromeoptions.add_argument('--headless')
chromeoptions.add_argument('--silent')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chromeoptions)
dateandtime = datetime.datetime.now()
products=[]
prices=[]
links=[]
conditions=[]
stocks=[]
sets=[]
maxpages=20
url='https://starcitygames.com/search/?sort=pricedesc&hawksearchable=search_includetext%3A%20%22default%22&instockonly=Yes&language=Japanese&mpp=96&pg='
print('Scrapping SCG Japanese stock')

for j in tqdm (range (1, maxpages), desc='Scrapping...'):
    finalurl=url + str(j)
    driver.get(finalurl)
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')

    for variants in soup.find_all('div', class_='hawk-results-item'):
        # name=variants.find('div', re.compile('_item_lnk2'))
        name=variants.find('h2', class_=('hawk-results-item__title'))
        findlink=name.find('a', href=True)
        link='https://starcitygames.com' + findlink['href']
        set=variants.find('p', class_=('hawk-results-item__category'))
        condition=(variants.find('div', class_='hawk-results-item__options-table-cell hawk-results-item__options-table-cell--name childCondition').text)[29:-2]
        price=variants.find('div', class_='hawk-results-item__options-table-cell hawk-results-item__options-table-cell--price childAttributes')
        stock=(variants.find('div', class_='hawk-results-item__options-table-cell hawk-results-item__options-table-cell--qty childAttributes').text)[5:]
        
        conditions.append(condition)
        products.append(name.text)
        prices.append(price.text)
        sets.append(set.text)
        stocks.append(stock)
        links+=[link]

newdf = pd.DataFrame({'Product':products, 'Set':sets, 'Condition':conditions, 'Price':prices, 'Stock':stocks, 'Link':links})
newdf.to_csv('scg-japanese-stock.csv')