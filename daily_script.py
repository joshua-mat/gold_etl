from datetime import datetime
import sqlite3, re


conn = sqlite3.connect('au_rate.sqlite')
cur = conn.cursor()

today = datetime.today().strftime("%Y-%m-%d")
cur.execute("INSERT OR REPLACE INTO gold_rates (date, price) VALUES (?, ?)", (today, float(gold_rate)))
conn.commit()
conn.close()