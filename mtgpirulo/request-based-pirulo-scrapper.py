import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import time

elapsedseconds = time.time()
requestheaders = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}
products=[]
prices=[]
links=[]
conditions=[]
sets=[]
maxpages=100
url='https://mtgpirulo.crystalcommerce.com/advanced_search?commit=Buscar&page='
urlending='&search%5Bbuy_price_gte%5D=&search%5Bbuy_price_lte%5D=&search%5Bcatalog_group_id_eq%5D=&search%5Bcategory_ids_with_descendants%5D%5B%5D=&search%5Bcategory_ids_with_descendants%5D%5B%5D=8&search%5Bdirection%5D=descend&search%5Bfuzzy_search%5D=&search%5Bin_stock%5D=1&search%5Bsell_price_gte%5D=&search%5Bsell_price_lte%5D=&search%5Bsort%5D=sell_price&search%5Btags_name_eq%5D=&search%5Bvariants_with_identifier%5D%5B14%5D%5B%5D=&search%5Bvariants_with_identifier%5D%5B15%5D%5B%5D=&search%5Bvariants_with_identifier%5D%5B15%5D%5B%5D=Japanese&search%5Bwith_descriptor_values%5D%5B10%5D=&search%5Bwith_descriptor_values%5D%5B11%5D=&search%5Bwith_descriptor_values%5D%5B1259%5D=&search%5Bwith_descriptor_values%5D%5B13%5D=&search%5Bwith_descriptor_values%5D%5B17023%5D=&search%5Bwith_descriptor_values%5D%5B348%5D=&search%5Bwith_descriptor_values%5D%5B361%5D=&search%5Bwith_descriptor_values%5D%5B6%5D=&search%5Bwith_descriptor_values%5D%5B7%5D=&search%5Bwith_descriptor_values%5D%5B9%5D=&utf8=%E2%9C%93'

print('Scrapping MTGPirulo Japanese cards')

for page in tqdm (range (1, maxpages), desc='Scrapping pages... '):
            finalurl=url + str(page) + urlending
            response = (requests.get(finalurl, requestheaders)).text
            soup = BeautifulSoup(response, 'html.parser')
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
                            link='https://www.mtgpirulo.com/products/search?q='+name
                            conditions+=[japanesecheck]
                            products+=[name]
                            prices+=[price]
                            sets+=[set]
                            links+=[link]
            else:
                print('No more pages to iterate!')
                break

newdf = pd.DataFrame({'Product':products, 'Price':prices, 'Condition':conditions, 'Set':sets, 'Link':links})
newdf.to_csv('MTGPirulo-japanese-stock.csv')
elapsedseconds = time.time() - elapsedseconds
print('Elapsed time: ' + str(int(elapsedseconds)) + ' seconds (' + str(elapsedseconds/60) + ' minutes).')
