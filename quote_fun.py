import random, os
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

client = MongoClient(os.getenv("LOGIN_DATA"))
db = client.Movies
quotes = db.quotes.find({})

#Quotes for a navbar
def quote():
    quotes_list =[]
    quotes = db.quotes.find({})
    for quo in quotes:
        quotes_list.append(quo['quote'])
    random_value = random.randint(1,151)
    return quotes_list[random_value]





    