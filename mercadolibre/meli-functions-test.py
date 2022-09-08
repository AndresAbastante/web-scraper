import requests
from bs4 import BeautifulSoup

requestheaders={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}
url='https://listado.mercadolibre.com.ar/pokemon-primera-edicion'

def html_into_soup(url,requestheaders):
    response=(requests.get(url, requestheaders)).text
    soup=BeautifulSoup(response, 'html.parser')
    return soup

print(html_into_soup(url,requestheaders))