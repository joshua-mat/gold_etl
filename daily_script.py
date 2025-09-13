from datetime import datetime
from bs4 import BeautifulSoup
from utils import format_date
import sqlite3,os, requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)
DB_PATH = os.path.join(BASE_DIR, "au_rate.sqlite")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

today = datetime.today().strftime("%Y-%m-%d")

print(f"Script started at {datetime.now()}")

url = "https://gulfnews.com/gold-forex/historical-gold-rates"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
priceTable = soup.find('table', class_='OSFry')
rows = list()
for data in priceTable.find_all('tbody'):
    rows = data.find_all('tr')
cur.execute("SELECT date FROM rate WHERE date = ?", (today,))
rowExists = cur.fetchone()

for i in range(len(rows)):
    cells = rows[i].find_all('td')
    date = format_date(cells[0].text)
    twoFourC = cells[1].text
    twoTwoC = cells[2].text
    twoOneC = cells[3].text
    oneEightC = cells[4].text
    if date == today and not rowExists:
        cur.execute('''INSERT OR IGNORE INTO rate (date, carat_24, carat_22, carat_21, carat_18)
               VALUES ( ?,?,?,?,? )''', (date, twoFourC, twoTwoC, twoOneC, oneEightC))
        print(f"✅ Updated DB with {today} rate for 18 c is {oneEightC}")
    else:
        print("todays date already updated")
    conn.commit()
    break
cur.execute("""
    DELETE FROM rate
    WHERE date NOT IN (
        SELECT date FROM rate
        ORDER BY date DESC
        LIMIT 20
    )
    """)
# sqlstr = "SELECT date, carat_18 FROM rate WHERE date = ?"
# for row in cur.execute(sqlstr, (today,)):
#     print(str(row[0]))
# conn.commit()
cur.close()