import sqlite3
db = sqlite3.connect("zhorro.db")

print("WORD:")
print(db.execute(
    "SELECT * FROM words WHERE word='что'"
).fetchall())

print("WORD_FILES:")
print(db.execute(
    "SELECT * FROM word_files WHERE word_id=1757355"
).fetchall())

print("FILES:")
print(db.execute(
    "SELECT * FROM files WHERE id=24"
).fetchall())

print("FULL JOIN:")
print(db.execute("""
    SELECT files.path
    FROM files
    JOIN word_files ON word_files.file_id = files.id
    JOIN words ON word_files.word_id = words.id
    WHERE words.word = 'что'
""").fetchall())

db.close()