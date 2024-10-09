from re import S
import requests
from bs4 import BeautifulSoup
from os.path import exists
import logging
import asyncio
import time
import aiohttp

##-----##
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}
products=[]
prices=[]
links=[]
tasks=[]
urlstxtfile='url.txt'
urlnumber=sum(1 for line in open(urlstxtfile,'r'))
maxitems=48
link="https://autos.mercadolibre.com.ar/dueno-directo/_OrderId_PRICE_PublishedToday_YES_NoIndex_True"

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
   a=siguiente['href']
  except ValueError:
   logging.info ("puto")
  return(a)

async def fetch(session, link):
 async with session.get(link) as response:
  return await response.text()

def scraper2(link):
 soup=html_response_into_soup(link)
 title = link
 return title

async def main():
 link="https://autos.mercadolibre.com.ar/dueno-directo/_Desde_900_OrderId_PRICE_PublishedToday_YES_NoIndex_True"
 while link!= '':
  link=link_gather(link)
 print(f"Found {len(links)} results")

 start_time = time.time()
 async with aiohttp.ClientSession() as session:
  tasks = [fetch(session, link) for link in links]
  return await asyncio.gather(*tasks)
 
 end_time = time.time()
 elapsed_time = end_time - start_time
 print(f"ASYNC took : {elapsed_time:.2f} seconds")

 start_time2 = time.time()
 for link in links:
  scraper2(link)
 end_time2 = time.time()
 elapsed_time2 = end_time2 - start_time2
 print(f"SYNC took: {elapsed_time2:.2f} seconds")
 
asyncio.run(main())