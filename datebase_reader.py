import sqlite3
import random, os
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

client = MongoClient(os.getenv("LOGIN_DATA"))
db = client.Movies

#Add movies made in year 2001 from datebase from imdb
con = sqlite3.connect('movies.db')
cur = con.cursor()

cur.execute("SELECT title FROM movies WHERE year=2001")

movies_2001 = cur.fetchall()

for movie in movies_2001:
    movie = movie[0]
    if len(movie) > 25:
                movie = movie[:25] + "..."
    else:
        movie
    db.movie.insert_one({"movie title": movie})


con.close()

