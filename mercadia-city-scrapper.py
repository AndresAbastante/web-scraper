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

    for variants in soup.find_all('div', class_='product details product-item-details'):
        name=variants.find('a', href=True, class_=('product-item-link'))
        link=name['href']
        condition=variants.find('div', class_='product description product-item-description')
        price=variants.find('span', class_='price')
        stockfilter=variants.find('div', class_='aw-cus__customstockstatus')
        stock=(stockfilter.find('div', class_='text').text)[6:]
        
        conditions.append(condition)
        products.append(name.text)
        prices.append(price.text)
        sets.append(set.text)
        stocks.append(stock)
        links+=[link]

newdf = pd.DataFrame({'Product':products, 'Set':sets, 'Condition':conditions, 'Price':prices, 'Stock':stocks, 'Link':links})
newdf.to_csv('Mercadia-City-japanese-stock.csv')