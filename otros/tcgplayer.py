from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import subprocess

url='https://www.tcgplayer.com/search/pokemon/base-set-shadowless?Price_Condition=Less+Than&advancedSearch=true&productLineName=pokemon&view=list&setName=base-set-shadowless&page=1&Condition=Lightly+Played&Printing=1st+Edition'
chromeOptions = Options()
chromeOptions.add_argument("--user-data-dir=C:\\Users\\Andres\\Users\\ataba\AppData\\Local\\Google\\Chrome\\User Data")

driver = webdriver.Chrome(options=chromeOptions)
driver.get(url)
time.sleep(200) 
content = driver.page_source
soup = BeautifulSoup(content, 'html.parser') #https://beautiful-soup-4.readthedocs.io/en/latest/
