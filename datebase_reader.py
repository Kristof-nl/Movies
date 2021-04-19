import sqlite3
import random, os
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

client = MongoClient(os.getenv("LOGIN_DATA"))
db = client.Movies

character_list = ["#", ".", ",", "{", "}", "\\", "^", "~",";", "/", "=","£","¤","¥","¦","¨","ª","«"]

#Add movies made in choosen year from imdb datebase
def add_movies(year):
    con = sqlite3.connect('movies.db')
    cur = con.cursor()

    cur.execute("SELECT title FROM movies WHERE year={}".format(year))

    movies_year = cur.fetchall()

    for movie in movies_year:
        movie = movie[0].capitalize()
        if movie[0] not in character_list:
            if len(movie) > 25:
                movie = movie[:25] + "..."
            else:
                movie
            db.movie.insert_one({"movie title": movie})


    con.close()


add_movies(1974)