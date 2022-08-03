import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import time
import datetime

elapsedseconds = time.time()
requestheaders = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}
products=[]
prices=[]
links=[]
maxpages=10000
melipagestep=50
urlnumber = sum(1 for line in open('meli-urls.txt','r'))

with open('meli-urls.txt','r') as f:
    for url in tqdm(f, total=urlnumber, desc='Scraping sites...'):
        print('Scraping ' + url)
        finalurl=url + '_Desde_1_NoIndex_True'
        response = (requests.get(finalurl, requestheaders)).text
        soup = BeautifulSoup(response, 'html.parser')
        formatcheck=soup.find('a', class_='ui-search-result__content ui-search-link')
        if formatcheck==None:
            print('casto A')
            for page in tqdm (range (1, maxpages, melipagestep), desc='Scraping pages... '):
                finalurl=url + '_Desde_' + str(page) + '_NoIndex_True'
                response = (requests.get(finalurl, requestheaders)).text
                soup = BeautifulSoup(response, 'html.parser')
                endsearchcheck=soup.find('div', class_='ui-search-rescue__info')
                if endsearchcheck==None:
                    for variants in soup.find_all('div', class_='ui-search-result__wrapper'):
                        name=variants.find('h2', class_='ui-search-item__title')
                        price=variants.find('span', class_='price-variants-fraction')
                        linkclass=variants.find('a', href=True, class_='ui-search-item__group__element ui-search-link')
                        link=linkclass['href']
                        products.append(name.text)
                        prices.append(price.text)
                        links+= [link]
                else:
                    print('No more pages to iterate!')
                    break
        else: #this should be checked
            print('casto B')
            for page in tqdm (range (1, maxpages), desc='Scraping pages... '):
                finalurl=url + '_Desde_' + str(page) + '_NoIndex_True'
                response = (requests.get(finalurl, requestheaders)).text
                soup = BeautifulSoup(response, 'html.parser')
                endsearchcheck=soup.find('div', class_='ui-search-rescue__info')
                if endsearchcheck==None:
                    for variants in soup.find_all('a', href=True, class_="ui-search-result__content ui-search-link"):
                        link=variants['href']
                        name=variants.find('h2', class_="ui-search-item__title")
                        price=variants.find('span', class_="price-tag-fraction")
                
                        products.append(name.text)
                        prices.append(price.text)
                        links+= [link]
                else:
                    print('No more pages to iterate!')
                    break
        newdf = pd.DataFrame({'Product':products, 'Price':prices, 'Link':links})
        newdf.to_csv(f)
        elapsedseconds = time.time() - elapsedseconds
        print('Elapsed time: ' + str(int(elapsedseconds)) + ' seconds (' + str(elapsedseconds/60) + ' minutes).')
