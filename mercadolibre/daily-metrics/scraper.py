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
zones = []; prices = []; titles = []; links = []; tasks = []; years = []; kmss = []; urls = []; descriptions = []
oldcsv = "old_links.csv"
highlightscsv = "highlights.csv"
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}

def html_response_into_soup(link):
  response=(requests.get(link, headers)).text
  soup=BeautifulSoup(response, 'html.parser')
  return soup

def link_gather(link):
  try:
    soup = html_response_into_soup(link)
  except ValueError:
    logging.info ("puto")
  print ('Scraping ' + link)
  for variants in soup.find_all('div', class_='ui-search-result__wrapper'):
    linkclass = variants.find('a', href=True, class_='')
    link = linkclass['href'].split('-_JM#',1)[0]
    links.append(link)
  siguiente = soup.find('a', class_='andes-pagination__link', title="Siguiente")
  if siguiente:
    try:
      link = siguiente['href']
    except ValueError:
      logging.error ("puto")
  return(link)

async def link_gather2(link):
  try:
    soup = BeautifulSoup(await session.get(link).text(), 'html.parser')
  except ValueError:
    logging.error ("puto")
  logging.info ('Scraping ' + link)
  for variants in soup.find_all('div', class_='ui-search-result__wrapper'):
    linkclass = variants.find('a', href=True, class_='')
    link = linkclass['href'].split('-_JM#',1)[0]
    links.append(link)
  siguiente = soup.find('a', class_='andes-pagination__link', title="Siguiente")
  if siguiente:
    try:
      link = siguiente['href']
    except ValueError:
      logging.info ("puto")
  return(link)

async def scraper(resp):
  try:
    soup = BeautifulSoup(await resp.text(), 'html.parser')
    header = soup.find('div', class_='ui-pdp-container__col col-2 ui-vip-core-container--short-description ui-vip-core-container--column__right')
    yearkms = header.find('span', class_='ui-pdp-subtitle')
    title = header.find('h1', class_='ui-pdp-title').text
    price_element = header.find('span', class_='andes-money-amount')
    price = price_element['aria-label']
    zone = soup.find('span', class_='ui-pdp-color--BLACK ui-pdp-size--SMALL ui-pdp-family--SEMIBOLD').text
    description = soup.find('p', class_='ui-pdp-description__content').text
    pattern = re.compile(r'(\d{4})\s*\|\s*([\d\.]+)\s*km')
    match = pattern.search(str(yearkms))
    if match and title:
      year = match.group(1)
      kms = match.group(2)
    else:
      logging.error ('No match for year and kms. Those will be set as "Null"')
      year = 'Null'
      kms = 'Null'
  except UnboundLocalError:
    year = 'Null'
    kms = 'Null'
    title = 'Null'
    description = 'Null'
    price = 'Null'
    zone = 'Null'
  finally:
    return title, year, kms, description, price, zone
   
async def main():
  link = "https://autos.mercadolibre.com.ar/dueno-directo/_OrderId_PRICE_PublishedToday_YES_NoIndex_True"
  while link!='':
    link = link_gather(link)
  logging.info (f"Found a total of {len(links)} results")
  newlinksdf = pd.DataFrame({'links':links})
  oldlinksdf = pd.read_csv(oldcsv, dtype={'Links':'string'})
  mergeddf = oldlinksdf.merge(newlinksdf, how='right', indicator='Exists')
  highlightslinksdf = mergeddf.query("Exists == 'right_only'")
  if highlightslinksdf.empty:
    logging.info ("No new results found.")
  else:
    logging.info (f"Found {len(highlightslinksdf)} new elements.")
    highlightslinksdf.drop('Exists', axis=1, inplace=True)
    session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False))
    for index, row in highlightslinksdf.iterrows():
      print(row['links'])
      async with session.get(row['links']) as resp:
        try:
          title, year, kms, price, zone, description = await scraper(resp)
          titles.append(title)
          years.append(year)
          kmss.append(kms)
          urls.append(row['links'])
          prices.append(price)
          zones.append(zone)
          descriptions.append(description)
        except UnboundLocalError:
          logging.error ("puto")
    mergeddf.drop('Exists', axis=1, inplace=True)
    newlinksdf.to_csv(oldcsv, index=False)
    highlightsdf = pd.DataFrame({'título':titles, 'año':years, 'kms':kmss, 'link':urls, 'precio':prices, 'zona':zones, 'descripción':descriptions})
    highlightsdf.to_csv(highlightscsv, index=False)
    
asyncio.run(main())