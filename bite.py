import sqlite3
db = sqlite3.connect("zhorro.db")

result = db.execute("SELECT sql FROM sqlite_master WHERE type = 'table'")

for row in result:
    print(row[0])

db.close()