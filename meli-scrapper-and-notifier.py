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
file = open('/Users/andresabastante/codigo/web-scrapper/urls.txt','r')
products=[]
prices=[]
links=[]
melipagestep=50
maxfinds=100

for i in file.readlines():

    url=i
    print("Scrapping " + url)
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    formatcheck=soup.find('a', class_="ui-search-result__content ui-search-link")

    if formatcheck==None:
        for j in tqdm (range (1, maxfinds, melipagestep), desc="Fetching..."):
            meliurl=url + "_Desde_" + str(i) + "_NoIndex_True"
            driver.get(meliurl)
            content = driver.page_source
            soup = BeautifulSoup(content, 'html.parser')
            endsearchcheck=soup.find('div', class_="ui-search-rescue__info")

            if endsearchcheck==None:
                for tag in soup.find_all('div', class_="ui-search-result__wrapper"):
                    name=tag.find('h2', class_="ui-search-item__title")
                    price=tag.find('span', class_="price-tag-fraction")
                    linkclass=tag.find('a', href=True, class_="ui-search-item__group__element ui-search-link")
                    link=linkclass['href']

                    products.append(name.text)
                    prices.append(price.text)
                    links+= [link]
            else:
                print("There are no more pages to iterate!")
                break
    else:
        for j in tqdm (range (1, maxfinds, melipagestep), desc="Fetching..."):
            meliurl=url + "_Desde_" + str(i) + "_NoIndex_True"
            driver.get(url)
            content = driver.page_source
            soup = BeautifulSoup(content, 'html.parser')
            endsearchcheck=soup.find('div', class_="ui-search-rescue__info")
            
            if endsearchcheck==None:
                for tag in soup.find_all('a', href=True, class_="ui-search-result__content ui-search-link"):
                    link=tag['href']
                    name=tag.find('h2', class_="ui-search-item__title")
                    price=tag.find('span', class_="price-tag-fraction")
            
                    products.append(name.text)
                    prices.append(price.text)
                    links+= [link]
            else:
                print("There are no more pages to iterate!")
                break

    dateandtime = datetime.datetime.now()
    excelfilename = "/Users/andresabastante/resultados-excel/meli-scraper-results-" + dateandtime.strftime("%y-%m-%d|%H;%M")+".csv"
    df = pd.DataFrame({'Producto':products, 'Precio':prices, 'Link':links})
    df.to_csv(excelfilename, index=False, encoding='utf-8')
    
    if df.empty==False:
        subprocess.call(['notify', '-bulk', '-i', excelfilename])