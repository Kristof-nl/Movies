import requests
from bs4 import BeautifulSoup


page = requests.get("http://www.planetofsuccess.com/blog/2019/movie-quotes/").text
soup = BeautifulSoup(page, 'html.parser')
soup2 = soup.find_all("blockquote")


quotes = []
for quote in soup.find_all("blockquote"):
    quo = quote.find('p').get_text().replace('\n','')
    quotes.append(quo)


        