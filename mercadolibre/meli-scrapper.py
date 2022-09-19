from re import S
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import subprocess
from os.path import exists
import os

#pd.options.mode.chained_assignment = None
requestheaders={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}
products=[]
prices=[]
links=[]
meliitemsstep=48
urlnumber=sum(1 for line in open('meli-urls.txt','r'))

def html_response_into_soup(url,requestheaders):
    response=(requests.get(url, requestheaders)).text
    soup=BeautifulSoup(response, 'html.parser')
    return soup

with open('meli-urls.txt','r') as f:
    maxitems=200
    for url in tqdm(f, total=urlnumber, desc='Scraping sites...'):
        print('Scraping ' + url)
        noresultscheck=html_response_into_soup(url,requestheaders).find('div', class_='ui-search-rescue__info')
        if noresultscheck==None:
            singlepagecheck=html_response_into_soup(url,requestheaders).find('li', class_='andes-pagination__page-count')
            if singlepagecheck==None:
                maxitems=48
            for pages in tqdm (range (1, maxitems, meliitemsstep), desc='Scraping pages... '):
                newurl=url + '_Desde_' + str(pages)
                for variants in html_response_into_soup(newurl,requestheaders).find_all('div', class_='ui-search-result__wrapper'):
                    name=variants.find('h2', class_='ui-search-item__title')
                    price=variants.find('span', class_='price-tag-fraction')
                    linkclass=variants.find('a', href=True, class_='ui-search-result__content ui-search-link')
                    if linkclass==None:
                        linkclass=variants.find('a', href=True, class_='ui-search-link')
                        if linkclass==None:
                            linkclass=variants.find('a', href=True, class_='ui-search-item__group__element ui-search-link')
                    link=linkclass['href'].split('#',1)[0]
                    products.append(name.text)
                    prices.append(price.text)
                    links += [link]
            filename=url.replace('https://','').replace('/','-').replace('\n','')+'.csv'
            tempdf=pd.DataFrame({'Product':products, 'Price':prices, 'Link':links})
            tempdffilename='new-' + filename
            if exists(filename):
                olddf=pd.read_csv(filename, dtype={'Product':'string','Price':'string','Link':'string'})
                tempdf.to_csv(tempdffilename, index=False)
                newdf=pd.read_csv(tempdffilename, dtype={'Product':'string','Price':'string','Link':'string'})
                mergeddf=olddf.merge(newdf, how='right', indicator='Exists')
                highlights=mergeddf.query("Exists == 'right_only'")
                if highlights.empty:
                    print('\n*** Same items found! D: ***')
                else:
                    print('\n*** New items found! :D ***')
                    highlights.drop('Exists', axis=1, inplace=True)
                    highlights.to_csv('new_items.csv', index=False)
                    mergeddf.drop('Exists', axis=1, inplace=True)
                    mergeddf.to_csv(filename, index=False)
                    subprocess.call(['notify', '-bulk', '-i', 'new_items.csv'])
                    os.remove('new_items.csv')
                os.remove(tempdffilename)
            else:
                print('\n*** New items found! :D ***')
                tempdf.to_csv(filename, index=False)
                subprocess.call(['notify', '-bulk', '-i', filename])
            products.clear()
            prices.clear()
            links.clear()
        else:
            print('*** No items listed! :O ***')