import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import time

print('Scrapping MercadiaCity Japanese stock')

elapsedseconds = time.time()
requestheaders = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}
products=[]
prices=[]
links=[]
conditions=[]
stocks=[]
sets=[]
maxpages=100
urlnumber = sum(1 for line in open('mercadia-city-urls.txt','r'))

with open('mercadia-city-urls.txt','r') as f:
    for url in tqdm(f, total=urlnumber, desc='Scrapping sites...'):
        
        for page in tqdm (range (1, maxpages), desc='Scrapping pages... '):
            finalurl= url + '&p=' + str(page)
            response = (requests.get(finalurl, requestheaders)).text
            soup = BeautifulSoup(response, 'html.parser')
            endsearchcheck=soup.find('div', class_='message info empty')
            if endsearchcheck==None:
                for variants in soup.find_all('div', class_='product details product-item-details'):
                    name=variants.find('a', href=True, class_=('product-item-link'))
                    link=name['href']
                    name=(name.text)[9:-7]
                    condition=(variants.find('div', class_='product description product-item-description').text)[8:-6]
                    price=(variants.find('span', class_='price').text)
                    
                    conditions.append(condition)
                    products.append(name)
                    prices.append(price)
                    links+=[link]
            else:
                print('No more pages to iterate!')
                break

newdf = pd.DataFrame({'Product':products, 'Price':prices, 'Condition':conditions, 'Link':links})
newdf.to_csv('Mercadia-City-japanese-stock.csv', index=False)
elapsedseconds = time.time() - elapsedseconds
print('Elapsed time: ' + str(int(elapsedseconds)) + ' seconds (' + str(elapsedseconds/60) + ' minutes).')