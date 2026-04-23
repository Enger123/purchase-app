import sqlite3
conn = sqlite3.connect('purs.db', check_same_thread=False)
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS purchases(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name str,
done INTEGER
)""")