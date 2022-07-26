from doctest import OutputChecker
from hashlib import new
from numpy import isin
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
maxpages=30
url='https://mtgpirulo.crystalcommerce.com/advanced_search?commit=Buscar&page='
print('Scrapping MTGPirulo Japanese cards')

for j in tqdm (range (29, maxpages), desc='Scrapping...'):
    finalurl=url + str(j) + '&search%5Bbuy_price_gte%5D=&search%5Bbuy_price_lte%5D=&search%5Bcatalog_group_id_eq%5D=&search%5Bcategory_ids_with_descendants%5D%5B%5D=&search%5Bcategory_ids_with_descendants%5D%5B%5D=8&search%5Bdirection%5D=descend&search%5Bfuzzy_search%5D=&search%5Bin_stock%5D=1&search%5Bsell_price_gte%5D=&search%5Bsell_price_lte%5D=&search%5Bsort%5D=sell_price&search%5Btags_name_eq%5D=&search%5Bvariants_with_identifier%5D%5B14%5D%5B%5D=&search%5Bvariants_with_identifier%5D%5B15%5D%5B%5D=&search%5Bvariants_with_identifier%5D%5B15%5D%5B%5D=Japanese&search%5Bwith_descriptor_values%5D%5B10%5D=&search%5Bwith_descriptor_values%5D%5B11%5D=&search%5Bwith_descriptor_values%5D%5B1259%5D=&search%5Bwith_descriptor_values%5D%5B13%5D=&search%5Bwith_descriptor_values%5D%5B17023%5D=&search%5Bwith_descriptor_values%5D%5B348%5D=&search%5Bwith_descriptor_values%5D%5B361%5D=&search%5Bwith_descriptor_values%5D%5B6%5D=&search%5Bwith_descriptor_values%5D%5B7%5D=&search%5Bwith_descriptor_values%5D%5B9%5D=&utf8=%E2%9C%93'
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

olddf = pd.read_csv('mtgpirulo-japanese-stock.csv')
csvfilename = 'mtgpirulo-new-results' + dateandtime.strftime('%y-%m-%d %H:%M') + '.csv'
newdf = pd.DataFrame({'Product':products, 'Price':prices, 'Condition':condition, 'Set':sets, 'Stock':stocks})
newdf.to_csv(csvfilename, index=True)
merged = pd.concat([olddf, newdf]).reset_index(drop=True)
merged.drop('Unnamed: 0', inplace=True, axis=1)
merged.to_csv('mtgpirulo-japanese-stock.csv')

#mergeddf.to_csv('merged' + dateandtime.strftime('%y-%m-%d %H:%M') + '.csv')

#subprocess.call(['open', 'merged.csv'])
#if df.empty==False:
#    subprocess.call(['notify', '-bulk', '-i', excelfilename])