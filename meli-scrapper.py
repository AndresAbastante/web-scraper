from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import datetime

chromeoptions=Options()
chromeoptions.add_argument("--headless")
driver = webdriver.Chrome("/opt/homebrew/bin/chromedriver", chrome_options=chromeoptions)
products=[]
prices=[]
links=[]
melipagestep=50

url="https://listado.mercadolibre.com.ar/repuestos/407"


for i in range(1, 2000, melipagestep):

    meliurl=url + "_Desde_" + str(i) + "_NoIndex_True"
    print(meliurl)
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')

    for a in soup.find_all('div', class_="ui-search-result__content-wrapper"):
        name=a.find('a', href=True, class_="ui-search-item__group__element ui-search-link")
        link=name['href']
        name=a.find('h2', class_="ui-search-item__title")
        price=a.find('span', class_="price-tag-fraction")
    
        products.append(name.text)
        prices.append(price.text)
        links+= [link]

dateandtime = datetime.datetime.now()
excelfilename = "/Users/andresabastante/resultados-excel/resultados repuestos 407 coupe " + dateandtime.strftime("%Y-%m-%d %H:%M:%S")+".csv"
df = pd.DataFrame({'Producto':products, 'Precio':prices, 'Link':links}) 
df.to_csv(excelfilename, index=False, encoding='utf-8')