import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import subprocess
from os.path import exists
import os

requestheaders={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}
products=[]
prices=[]
links=[]
url="https://departamento.mercadolibre.com.ar/MLA-1425728423-dpto-venta-2-ambientes-con-balcon-centro-caseros-pozo-_JM"

def html_response_into_soup(url,requestheaders):
	response=(requests.get(url, requestheaders)).text
	soup=BeautifulSoup(response, 'html.parser')
	return soup

description=html_response_into_soup(url,requestheaders).find('p', class_='ui-pdp-description__content')
if description!=None:
	print(description)
	print("************")
	if "ANTICIPO" in description.text:
		exclusion="true"
	else:
		exclusion="false"
	print(exclusion)