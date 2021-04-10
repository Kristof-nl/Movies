import sqlite3

con = sqlite3.connect('movies.db')
cur = con.cursor()

cur.execute("SELECT title FROM movies WHERE year=2001")

movies_2001 = cur.fetchall()

print(movies_2001)


con.close()

