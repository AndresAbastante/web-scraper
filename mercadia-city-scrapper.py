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

print('Scrapping MercadiaCity Japanese stock')

urlnumber = sum(1 for line in open('mercadia-city-urls.txt','r'))
with open('mercadia-city-urls.txt','r') as f:
    for url in tqdm(f, total=urlnumber):
        print(url)
        driver.get(url)
        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')

        for variants in soup.find_all('div', class_='product details product-item-details'):
            name=variants.find('a', href=True, class_=('product-item-link'))
            link=name['href']
            name=(name.text)[9:-7]
            condition=(variants.find('div', class_='product description product-item-description').text)[8:-6]
            price=variants.find('span', class_='price')
            stockfilter=(variants.find('div', class_='aw-cus__customstockstatus').text)

            conditions.append(condition)
            products.append(name)
            prices.append(price.text)
            stocks.append(stockfilter)
            links+=[link]

newdf = pd.DataFrame({'Product':products, 'Condition':conditions, 'Price':prices, 'Stock':stocks, 'Link':links})
newdf.to_csv('Mercadia-City-japanese-stock.csv')