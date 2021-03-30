import requests, os
from bs4 import BeautifulSoup
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

client = MongoClient(os.getenv("LOGIN_DATA"))
db = client.Movies



page = requests.get("http://www.planetofsuccess.com/blog/2019/movie-quotes/").text
soup = BeautifulSoup(page, 'html.parser')

print(soup)

for quote in soup.find_all("blockquote"):
    quo = quote.find('p').get_text().replace('\n','')
    db.quotes.insert_one({"quote": quo})