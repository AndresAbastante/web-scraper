from re import S
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import subprocess
from os.path import exists
import os

requestheaders={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}
products=[]
prices=[]
links=[]
meliitemsstep=48
urlstxtfile='meli-urls.txt'
urlnumber=sum(1 for line in open(urlstxtfile,'r'))
maxitems=48
pricefilter=10000

def html_response_into_soup(url,requestheaders):
	response=(requests.get(url, requestheaders)).text
	soup=BeautifulSoup(response, 'html.parser')
	return soup

def pull_publication_values():
 global links
 price=variants.find('span', class_='andes-money-amount__fraction')
 if int(float(price.text.replace(".", ""))) > pricefilter:
  linkclass=variants.find('a', href=True, class_='poly-component__title')
  link=linkclass['href'].split('-_JM#',1)[0]
  name=variants.find('h2', class_='poly-box')
  products.append(name.text)
  prices.append(f'${price.text}')
  links += [link]

with open(urlstxtfile,'r') as f:
	for url in tqdm(f, total=urlnumber, desc='Scraping sites...'):
		print('Scraping ' + url)
		noresultscheck=html_response_into_soup(url,requestheaders).find('div', class_='ui-search-rescue__info')
		if noresultscheck!=None:
			print(f'\n{" No items listed! :O ":#^100}')
		else:
			pagescheck=html_response_into_soup(url,requestheaders).find('li', class_='andes-pagination__page-count')
			if pagescheck==None:
				pageamount=1
			else:
				pageamount=int(pagescheck.text.split(" ")[1])
			for page in tqdm (range (pageamount), desc='Scraping pages... '):
				newurl=url + '_Desde_' + str(page * meliitemsstep)
				variants=None
				for variants in html_response_into_soup(newurl,requestheaders).find_all('div', class_='ui-search-result__wrapper'):
					pull_publication_values()
				for variants in html_response_into_soup(newurl,requestheaders).find_all('a', href=True, class_='promotion-item__link-container'):
					pull_publication_values()
				for variants in html_response_into_soup(newurl,requestheaders).find_all('div', class_='ui-search-result__wrapper shops__result-wrapper'):
					pull_publication_values() 
			filename=url.replace('https://','').replace('?','').replace('/','-').replace('.','').replace('www','').replace('com','').replace('ar','').replace('=','').replace('_','-').replace('&','').replace('=','')
			filename = f"{filename[:45]}.csv"
			tempdf=pd.DataFrame({'Product':products, 'Price':prices, 'Link':links})
			tempdffilename=f'new-{filename}'
			if exists(filename):
				olddf=pd.read_csv(filename, dtype={'Product':'string','Price':'string','Link':'string'})
				tempdf.to_csv(tempdffilename, index=False)
				newdf=pd.read_csv(tempdffilename, dtype={'Product':'string','Price':'string','Link':'string'})
				mergeddf=olddf.merge(newdf, how='right', indicator='Exists')
				highlights=mergeddf.query("Exists == 'right_only'")
				if highlights.empty:
					print(f'\n{" Same items found! D: ":#^100}')
				else:
					print(f'\n{" New items found! :D ":#^100}')
					highlights.drop('Exists', axis=1, inplace=True)
					highlights.to_csv('new_items.csv', index=False)
					mergeddf.drop('Exists', axis=1, inplace=True)
					mergeddf.to_csv(filename, index=False)
					subprocess.call(['notify', '-i', 'new_items.csv'])
					os.remove('new_items.csv')
				os.remove(tempdffilename)
			else:
				print(f'\n{" New items found! :D ":#^100}')
				tempdf.to_csv(filename, index=False)
				subprocess.call(['notify', '-i', filename])
			products.clear()
			prices.clear()
			links.clear()