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
urlstxtfile='meli-lightning-urls.txt'
urlnumber=sum(1 for line in open(urlstxtfile,'r'))
maxitems=48
pageammount=4

def html_response_into_soup(url,requestheaders):
	response=(requests.get(url, requestheaders)).text
	soup=BeautifulSoup(response, 'html.parser')
	return soup

with open(urlstxtfile,'r') as f:
	for url in tqdm(f, total=urlnumber, desc='Scraping sites...'):
		print('Scraping ' + url)
		noresultscheck=html_response_into_soup(url,requestheaders).find('div', class_='ui-search-rescue__info')
		if noresultscheck==None:
			for page in tqdm (range (pageammount), desc='Scraping pages... '):
				newurl=url + str(page)
				variants=None
				for variants in html_response_into_soup(newurl,requestheaders).find_all('a', href=True, class_='promotion-item__link-container'):
					price=variants.find('span', class_='andes-money-amount__fraction')
					name=variants.find('p', class_='promotion-item__title')
					link=variants['href'].split('#',1)[0]
					products.append(name.text)
					prices.append(f'${price.text}')
					links += [link]
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
					subprocess.call(['notify', '-silent', '-i', 'new_items.csv'])
					os.remove('new_items.csv')
				os.remove(tempdffilename)
			else:
				print(f'\n{" New items found! :D ":#^100}')
				tempdf.to_csv(filename, index=False)
				subprocess.call(['notify', '-silent', '-i', filename])
			products.clear()
			prices.clear()
			links.clear()
		else:
						print(f'\n{" No items listed! :O ":#^100}')