import aiohttp
import asyncio
import csv
from bs4 import BeautifulSoup
import re
import pandas as pd

titles=[]
years=[]
kmss=[]
links2=[]

async def scraper(resp):
 soup = BeautifulSoup(await resp.text(), 'html.parser')
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
    async with aiohttp.ClientSession() as session:
        session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) 
        with open('old_links.csv', newline='') as csvfile:
            csvreader=csv.DictReader(csvfile)
            for link in csvreader:
                async with session.get(link['links']) as resp:
                    title, year, kms,  = await scraper(resp)
                    print(title)
                    titles.append(title)
                    years.append(year)
                    kmss.append(kms)
                    links2.append(link)
            resultsdf=pd.DataFrame({'title':titles, 'year':years, 'kmss':kmss})
            resultsdf.to_csv('results.csv', index=False)

asyncio.run(main())