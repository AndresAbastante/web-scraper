from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import subprocess
from tqdm import tqdm

chromeoptions=Options()
chromeoptions.add_argument('--headless')
chromeoptions.add_argument('--silent')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chromeoptions)
dateandtime = datetime.datetime.now()
products=[]
prices=[]
links=[]
condition=[]
stocks=[]
sets=[]
maxpages=50
url='https://starcitygames.com/search/?sort=pricedesc&hawksearchable=search_includetext%3A%20%22default%22&instockonly=Yes&language=Japanese&mpp=96&pg='
print('Scrapping MTGPirulo Japanese cards')

for j in tqdm (range (1, maxpages), desc='Scrapping...'):
    finalurl=url + str(j)
    driver.get(finalurl)
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    endsearchcheck=soup.find('p', class_='no-product')
    
    if endsearchcheck==None:
        for variants in soup.find_all('div', class_='variant-row row'):
            stock=(variants.find('span', class_='variant-short-info variant-qty').text)[66:-71]
            for tag in variants.find_all('form', class_='add-to-cart-form'):
                japanesecheck=tag['data-variant']
                if 'Japanese' in japanesecheck:
                    name=tag['data-name']
                    price=tag['data-price']
                    set=tag['data-category']
                    condition+=[japanesecheck]
                    products+=[name]
                    prices+=[price]
                    sets+=[set]
                    stocks+=[stock]
    else:
        print('There are no more pages to iterate!')
        break

#olddf = pd.read_csv('mtgpirulo-japanese-stock.csv')
#csvfilename = 'mtgpirulo-new-results' + dateandtime.strftime('%y-%m-%d %H:%M') + '.csv'
newdf = pd.DataFrame({'Product':products, 'Price':prices, 'Condition':condition, 'Set':sets, 'Stock':stocks})
newdf.to_csv('mtgpirulo-japanese-stock')
#newdf=pd.read_csv(csvfilename)

#mergeddf.to_csv('merged' + dateandtime.strftime('%y-%m-%d %H:%M') + '.csv')

#subprocess.call(['open', 'merged.csv'])
#if df.empty==False:
#    subprocess.call(['notify', '-bulk', '-i', excelfilename])