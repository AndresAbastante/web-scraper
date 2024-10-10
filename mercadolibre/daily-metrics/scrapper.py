from re import S
import requests
from bs4 import BeautifulSoup
from os.path import exists
import logging
import asyncio
import time
import aiohttp
import re
import pandas as pd
import csv
##-----##
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}
titles=[]
links=[]
tasks=[]
years=[]
kmss=[]
links2=[]
urlstxtfile='url.txt'
urlnumber=sum(1 for line in open(urlstxtfile,'r'))
maxitems=48
link="https://autos.mercadolibre.com.ar/dueno-directo/_OrderId_PRICE_PublishedToday_YES_NoIndex_True"
oldcsv="old_links.csv"

def html_response_into_soup(link):
	response=(requests.get(link, headers)).text
	soup=BeautifulSoup(response, 'html.parser')
	return soup

def link_gather(link):
 soup=html_response_into_soup(link)
 print ('Scraping ' + link)
 for variants in soup.find_all('div', class_='ui-search-result__wrapper'):
  linkclass=variants.find('a', href=True, class_='')
  link=linkclass['href'].split('-_JM#',1)[0]
  links.append(link)
 siguiente=soup.find('a', class_='andes-pagination__link', title="Siguiente")
 if siguiente:
  try:
   link=siguiente['href']
  except ValueError:
   logging.info ("puto")
  return(link)

async def fetch(session, link):
 async with session.get(link) as response:
  return await response.text()

def scraper(link):
 soup=html_response_into_soup(link)
 header=soup.find('div', class_='ui-pdp-container__col col-2 ui-vip-core-container--short-description ui-vip-core-container--column__right')
 yearkms=header.find('span', class_='ui-pdp-subtitle')
 title=header.find('h1', class_='ui-pdp-title').text
 pattern=re.compile(r'(\d{4})\s*\|\s*([\d\.]+)\s*km')
 match=pattern.search(str(yearkms))
 if match and title:
  year=match.group(1)
  kms=match.group(2)
 else:
  logging.error ('No match for year and kms. Those will be set as "Null"')
  year='Null'
  kms='Null'
 return title, year, kms
   
async def main():
 link="https://autos.mercadolibre.com.ar/dueno-directo/_Desde_1100_OrderId_PRICE_PublishedToday_YES_NoIndex_True"
 while link!= '':
  link=link_gather(link)
 print(f"Found a total of {len(links)} results")
 newdf=pd.DataFrame({'links':links})
 if exists(oldcsv):
  olddf=pd.read_csv(oldcsv, dtype={'Links':'string'})
  mergeddf=olddf.merge(newdf, how='right', indicator='Exists')
  highlights=mergeddf.query("Exists == 'right_only'")
  if highlights.empty:
   logging.info ("No new results found.")
  else:
   print(f'\n{" New items found! :D ":#^100}')
   highlights.drop('Exists', axis=1, inplace=True)
   highlights.to_csv(oldcsv, index=False)
 with open(oldcsv, newline='') as csvfile:
  csvreader=csv.DictReader(csvfile)
  for link in csvreader:
   print(link['links'])
   title, year, kms,  = scraper(link['links'])
   titles.append(title)
   years.append(year)
   kmss.append(kms)
   links2.append(link)
  resultsdf=pd.DataFrame({'title':titles, 'year':years, 'kmss':kmss})
  resultsdf.to_csv('results.csv', index=False)
asyncio.run(main())