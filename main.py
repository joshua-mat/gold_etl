from bs4 import BeautifulSoup
from datetime import datetime
import requests, re, sqlite3

def format_date(raw_date):
    cleaned_date = re.sub(r'(st|nd|rd|th)', '', raw_date)
    cleaned_date = cleaned_date.replace("Sept", "Sep")
    # Parse to datetime
    date_obj = datetime.strptime(cleaned_date.strip(), "%d %b %Y")
    formatted_date = date_obj.strftime("%Y-%m-%d")
    return formatted_date

conn = sqlite3.connect('au_rate.sqlite')
cur = conn.cursor()

cur.executescript('''
CREATE TABLE IF NOT EXISTS rate (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    date TEXT UNIQUE,
    carat_24 TEXT,
    carat_22 TEXT,
    carat_21 TEXT,
    carat_18 TEXT
);''')

url = "https://gulfnews.com/gold-forex/historical-gold-rates"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
priceTable= soup.find('table', class_='OSFry')
rows = list()
for data in priceTable.find_all('tbody'):
    rows = data.find_all('tr')

for row in rows:
    cells = row.find_all('td')
    date =  format_date( cells[0].text)
    twoFourC = cells[1].text
    twoTwoC = cells[2].text
    twoOneC = cells[3].text
    oneEightC = cells[4].text
    ## input into database
    cur.execute('''INSERT OR IGNORE INTO rate (date, carat_24, carat_22, carat_21, carat_18) 
               VALUES ( ?,?,?,?,? )''', (date, twoFourC, twoTwoC, twoOneC, oneEightC))

    conn.commit()

sqlstr = '''SELECT carat_18 FROM rate ORDER BY date DESC LIMIT 10'''

# for row in cur.execute(sqlstr):
#     print(str(row[0]))
cur.close()

