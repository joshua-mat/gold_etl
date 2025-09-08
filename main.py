import urllib.request
from bs4 import BeautifulSoup
import ssl
import requests

# ctx = ssl.create_default_context()
# ctx.check_hostname = False
# ctx.verify = False

url = "https://gulfnews.com/gold-forex/historical-gold-rates"
# html = urllib.request.urlopen(url, context=ctx).read()
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
priceTable= soup.find('table', class_='OSFry')

for data in priceTable.find_all('tbody'):
    rows = data.find_all('tr')
    print(rows[0])
    for row in rows:
        cells = row.find_all('td')
        print(cells)