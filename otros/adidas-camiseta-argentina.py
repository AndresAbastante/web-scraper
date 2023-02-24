from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import subprocess

chromeoptions=webdriver.ChromeOptions()
chromeoptions.add_argument('--disable-extentions')
chromeoptions.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), chrome_options=chromeoptions)
url='https://www.adidas.com.ar/camiseta-titular-argentina-3-estrellas-2022/IB3593.html'
#url='https://www.adidas.com.ar/camiseta-titular-argentina-22/HB9215.html?pr=oos_rr&slot=1&rec=mt'
time.sleep(1)
driver.get(url)
time.sleep(1) 
content = driver.page_source
soup = BeautifulSoup(content, 'html.parser') #https://beautiful-soup-4.readthedocs.io/en/latest/

agotado=soup.find('h3', class_='heading___2aqN2')
if agotado==None:
    subprocess.call(['notify', '-silent', '-i', 'message.txt'])