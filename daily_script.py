from datetime import datetime
from bs4 import BeautifulSoup
from main import format_date
import sqlite3, re
import requests

conn = sqlite3.connect('au_rate.sqlite')
cur = conn.cursor()

today = datetime.today().strftime("%Y-%m-%d")

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
        print(f"✅ Updated DB with {today}")
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
conn.commit()
conn.close()



# for row in rows:
#     cells = row.find_all('td')
#     date = format_date(cells[0].text)
#     twoFourC = cells[1].text
#     twoTwoC = cells[2].text
#     twoOneC = cells[3].text
#     oneEightC = cells[4].text
#     ## input into database
#     if date == today and not rowExists:
#         cur.execute('''INSERT OR IGNORE INTO rate (date, carat_24, carat_22, carat_21, carat_18)
#                VALUES ( ?,?,?,?,? )''', (date, twoFourC, twoTwoC, twoOneC, oneEightC))
#         print(f"✅ Updated DB with {today}")
#     else:
#         print("todays date already updated")
#
#     conn.commit()
# cur.execute("""
#     DELETE FROM rate
#     WHERE date NOT IN (
#         SELECT date FROM rate
#         ORDER BY date DESC
#         LIMIT 20
#     )
#     """)
# conn.commit()
# conn.close()