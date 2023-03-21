from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import os
import subprocess

#webdriver set up.
chromeoptions=webdriver.ChromeOptions()
chromeoptions.add_argument('--disable-extentions')
chromeoptions.add_argument('--start-maximized')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), chrome_options=chromeoptions)
url='https://www.ebay.com/mye/myebay/v2/purchase?page=1&moduleId=122169&mp=purchase-module-v2&type=v2&pg=purchase'

time.sleep(1)
driver.get(url)
time.sleep(60) 
content = driver.page_source
soup = BeautifulSoup(content, 'html.parser') #https://beautiful-soup-4.readthedocs.io/en/latest/

for items in soup.find_all('div', class_='m-ph-card__content m-ph-layout-row-hidable'):
    price= items.find('span', class_='BOLD')
    ordernumber=items.find('span', class_="primary__item--item-text")
    <a _sp="p3748097.m122169.l2648" aria-hidden="true" href="https://www.ebay.com/itm/334747133863" tabindex="-1">
    item_href=items.find('div', class_='m-image')

    item=item_href['src']