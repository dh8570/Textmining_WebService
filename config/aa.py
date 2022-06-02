
import sqlite3

conn = sqlite3.connect("db.sqlite3")
cur = conn.cursor()
cur.execute("SELECT * from django_session")
rows = cur.fetchall()
for row in rows:
    print(row)

conn.close()

