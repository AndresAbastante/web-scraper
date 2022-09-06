from asyncio.windows_events import NULL
import requests
from bs4 import BeautifulSoup

requestheaders={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}
url='https://listado.mercadolibre.com.ar/pokemon-primera-edicion'
response=(requests.get(url, requestheaders)).text
soup=BeautifulSoup(response, 'html.parser')
pages=soup.find('a', class_='andes-pagination')
print(pages)
