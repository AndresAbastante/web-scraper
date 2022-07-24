from typing import final
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
chromeoptions.add_argument("--headless")
chromeoptions.add_argument("--silent")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chromeoptions)
products=[]
prices=[]
links=[]
maxpages=10000
url="https://mtgpirulo.crystalcommerce.com/advanced_search?commit=Buscar&page="
print("Scrapping MTGPirulo Japanese finds")
driver.get(url)
content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')

for j in tqdm (range (1, maxpages), desc="Fetching..."):
    finalurl=url + str(i) + "&search%5Bbuy_price_gte%5D=&search%5Bbuy_price_lte%5D=&search%5Bcatalog_group_id_eq%5D=&search%5Bcategory_ids_with_descendants%5D%5B%5D=&search%5Bcategory_ids_with_descendants%5D%5B%5D=8&search%5Bdirection%5D=descend&search%5Bfuzzy_search%5D=&search%5Bin_stock%5D=1&search%5Bsell_price_gte%5D=&search%5Bsell_price_lte%5D=&search%5Bsort%5D=sell_price&search%5Btags_name_eq%5D=&search%5Bvariants_with_identifier%5D%5B14%5D%5B%5D=&search%5Bvariants_with_identifier%5D%5B15%5D%5B%5D=&search%5Bvariants_with_identifier%5D%5B15%5D%5B%5D=Japanese&search%5Bwith_descriptor_values%5D%5B10%5D=&search%5Bwith_descriptor_values%5D%5B11%5D=&search%5Bwith_descriptor_values%5D%5B1259%5D=&search%5Bwith_descriptor_values%5D%5B13%5D=&search%5Bwith_descriptor_values%5D%5B17023%5D=&search%5Bwith_descriptor_values%5D%5B348%5D=&search%5Bwith_descriptor_values%5D%5B361%5D=&search%5Bwith_descriptor_values%5D%5B6%5D=&search%5Bwith_descriptor_values%5D%5B7%5D=&search%5Bwith_descriptor_values%5D%5B9%5D=&utf8=%E2%9C%93"
    driver.get(finalurl)
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    endsearchcheck=soup.find('p', class_="no-product")
    
    if endsearchcheck==None:    
        for tag in soup.find_all('form', class_="add-to-cart-form"):
            name=tag.find('h2', class_="ui-search-item__title")
            price=tag.find('span', class_="regular price")
            linkclass=tag.find('a', href=True, class_="ui-search-item__group__element ui-search-link")
            link=linkclass['href']
    
        products.append(name.text)
        prices.append(price.text)
        links+= [link]
    else:
                print("There are no more pages to iterate!")
                break

dateandtime = datetime.datetime.now()
excelfilename = "MTGPirulo-scraper-results-" + dateandtime.strftime("%y-%m-%d %H:%M")+".csv"
df = pd.DataFrame({'Producto':products, 'Precio':prices, 'Link':links})
df.to_csv(excelfilename, index=False, encoding='utf-8')

if df.empty==False:
    subprocess.call(['notify', '-bulk', '-i', excelfilename])