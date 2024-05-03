import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO users (username, hash) VALUES (?, ?)", ('Example1', 'DummyHash'))
cur.execute("INSERT INTO users (username, hash) VALUES (?, ?)", ('Example2', 'DummyHash2'))

connection.commit()
connection.close()