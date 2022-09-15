from re import S
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import time
import subprocess
from os.path import exists
import os

elapsedseconds=time.time()
requestheaders={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}
products=[]
prices=[]
links=[]
meliitemsstep=49
urlnumber=sum(1 for line in open('meli-urls.txt','r'))
dfheader=['Product', 'Price', 'Link']
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

                filename=url.replace('https://','').replace('/','-').replace('\n','-')+'.csv'
                tempdf=pd.DataFrame({'Product':products, 'Price':prices, 'Link':links})
                tempdffilename='new-' + filename
                if exists(filename):
                    print('***There is a previous input***')
                    olddf=pd.read_csv(filename, dtype={"Price":"string"})
                    tempdf.to_csv(tempdffilename, index=False, columns=dfheader)
                    newdf=pd.read_csv(tempdffilename, dtype={"Price":"string"})
                    mergeddf=pd.merge(olddf, newdf, on=['Product', 'Price'], how="right", indicator="Exist")
                    highlights=mergeddf.query("Exist == 'right_only'")
                    if highlights.empty:
                        print('***There were no changes since the last iteration***')
                    else:
                        print("***There were new items found since last iteration***")
                        highlights.drop(highlights.columns[[2, 4]], axis=1, inplace=True)
                        highlights.columns=dfheader
                        highlights.to_csv('new_items.csv', index=False, columns=dfheader)
                        mergeddf.drop(mergeddf.columns[[2, 4]], axis=1, inplace=True)
                        mergeddf.columns=dfheader
                        mergeddf.to_csv(filename, index=False, columns=dfheader)
                        subprocess.call(['notify', '-bulk', '-i', 'new_items.csv'])
                        os.remove('new_items.csv')
                    os.remove(tempdffilename)
                else:
                    print('***There was not a previous input***')
                    tempdf.to_csv(filename, index=False)
                    subprocess.call(['notify', '-bulk', '-i', filename])
                products.clear()
                prices.clear()
                links.clear()
        else:
            print('***No results were found!***')
elapsedseconds=time.time() - elapsedseconds
print('Elapsed time: ' + str(int(elapsedseconds)) + ' seconds (' + str(elapsedseconds/60) + ' minutes).')