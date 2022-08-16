from hashlib import new
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import time

url='https://checkout.bidcom.com.ar/Cart/set_cart?id='

elapsedseconds=time.time()
requestheaders={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}
products=[]
prices=[]
links=[]
maxitems=10000

for pages in tqdm (range (1, maxitems), desc='Scraping pages... '):
    filledpage=str(pages).zfill(5)
    print(filledpage)
    finalurl=url + filledpage + '&q=1&to=gadnic&cp='
    response=(requests.get(finalurl, requestheaders)).text
    soup=BeautifulSoup(response, 'html.parser')

    for variants in soup.find_all('div', class_='row row-item-cart'):
        name=(variants.find('div', class_='titulo-producto-cart')).text[29:-25]
        price=variants.find('div', class_='col-md-5 precio-cart text-right')
        products.append(name)
        prices.append(price.text)
        links.append(finalurl)

temporarydf=pd.DataFrame({'Product':products, 'Price':prices, 'Link':links})
filename=url.replace('https://','').replace('/','-')+'.csv'
temporarydf.to_csv(filename)
products.clear()
prices.clear()
links.clear()
elapsedseconds=time.time() - elapsedseconds
print('Elapsed time: ' + str(int(elapsedseconds)) + ' seconds (' + str(elapsedseconds/60) + ' minutes).')        