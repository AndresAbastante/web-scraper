import requests

url='https://www2.jus.gov.ar/dnrpa-site/#!/estimador'

response=requests.get(url)

response.cookies

for cookie in response.cookies:
    print(cookie.name, cookie.domain, cookie.value)