from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import subprocess

chromeoptions=Options()
chromeoptions.add_argument("--headless")
driver = webdriver.Chrome("/opt/homebrew/bin/chromedriver", chrome_options=chromeoptions)
products=[]
prices=[]
links=[]
melipagestep=50
search=input("Input MeLi search")
url="https://listado.mercadolibre.com.ar/" + search

for i in range(1, 10000, melipagestep):

    meliurl=url + "_Desde_" + str(i) + "_NoIndex_True"
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    
    #MeLi uses different formating depending on which items you are searching for. This checks which format //
    #is currently being used.
    
    formatcheck=soup.find('a', class_="ui-search-result__content ui-search-link")
    print(formatcheck)
    if formatcheck==None:
        for tag in soup.find_all('div', class_="ui-search-result__wrapper"):
            name=tag.find('h2', class_="ui-search-item__title")
            price=tag.find('span', class_="price-tag-fraction")
            linkclass=tag.find('a', href=True, class_="ui-search-item__group__element ui-search-link")
            link=linkclass['href']

            products.append(name.text)
            prices.append(price.text)
            links+= [link]
    else:
        for tag in soup.find_all('a', href=True, class_="ui-search-result__content ui-search-link"):
            link=tag['href']
            name=tag.find('h2', class_="ui-search-item__title")
            price=tag.find('span', class_="price-tag-fraction")
    
            products.append(name.text)
            prices.append(price.text)
            links+= [link]

dateandtime = datetime.datetime.now()
excelfilename = "/Users/andresabastante/resultados-excel/results " + search + " " + dateandtime.strftime("%Y-%m-%d %H:%M:%S")+".csv"
df = pd.DataFrame({'Producto':products, 'Precio':prices, 'Link':links}) 
df.to_csv(excelfilename, index=False, encoding='utf-8')
subprocess.call(['open', excelfilename])