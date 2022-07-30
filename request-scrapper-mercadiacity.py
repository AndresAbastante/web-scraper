import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}
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
        response = (requests.get(url, headers)).text
        print('response: ' + response)
        soup = BeautifulSoup(response, 'html.parser')
        for variants in soup.find_all('div', class_='product details product-item-details'):
            name=variants.find('a', href=True, class_=('product-item-link'))
            link=name['href']
            name=(name.text)[9:-7]
            condition=(variants.find('div', class_='product description product-item-description').text)[8:-6]
            price=variants.find('span', class_='price')
            stock=(variants.find('div', class_='aw-cus__customstockstatus').text)

            conditions.append(condition)
            products.append(name)
            prices.append(price.text)
            stocks.append(stock)
            links+=[link]

newdf = pd.DataFrame({'Product':products, 'Condition':conditions, 'Price':prices, 'Stock':stocks, 'Link':links})
newdf.to_csv('Mercadia-City-japanese-stock.csv')