from re import S
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import time
import subprocess

elapsedseconds=time.time()
requestheaders={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}
products=[]
prices=[]
links=[]
meliitemsstep=49
urlnumber=sum(1 for line in open('meli-urls.txt','r'))

def html_response_into_soup(url,requestheaders):
    response=(requests.get(url, requestheaders)).text
    soup=BeautifulSoup(response, 'html.parser')
    return soup

with open('meli-urls.txt','r') as f:
    maxitems=1000
    for url in tqdm(f, total=urlnumber, desc='Scraping sites...'):
        print('Scraping ' + url)
        noresultscheck=html_response_into_soup(url,requestheaders).find('div', class_='ui-search-rescue__info')
        if noresultscheck==None:
            singlepagecheck=html_response_into_soup(url,requestheaders).find('a', class_='andes-pagination')
            if singlepagecheck==None:
                maxitems=49
            for pages in tqdm (range (1, maxitems, meliitemsstep), desc='Scraping pages... '):
                url=url + '_Desde_' + str(pages)
                for variants in html_response_into_soup(url,requestheaders).find_all('div', class_='ui-search-result__wrapper'):
                    name=variants.find('h2', class_='ui-search-item__title')
                    price=variants.find('span', class_='price-tag-fraction')
                    linkclass=variants.find('a', href=True, class_='ui-search-result__content ui-search-link')
                    if linkclass==None:
                        linkclass=variants.find('a', href=True, class_='ui-search-link')
                        if linkclass==None:
                            linkclass=variants.find('a', href=True, class_='ui-search-item__group__element ui-search-link')
                    link=linkclass['href']
                    products.append(name.text)
                    prices.append(price.text)
                    links += [link]
        temporarydf=pd.DataFrame({'Product':products, 'Price':prices, 'Link':links})
        filename=url.replace('https://','').replace('/','-').replace('\n','-')+'.csv'
        if temporarydf.empty==False:
            temporarydf.to_csv(filename)
            #subprocess.call(['notify', '-bulk', '-i', filename])
        else:
            print('***No results were found!***')
        products.clear()
        prices.clear()
        links.clear()
elapsedseconds=time.time() - elapsedseconds
print('Elapsed time: ' + str(int(elapsedseconds)) + ' seconds (' + str(elapsedseconds/60) + ' minutes).')