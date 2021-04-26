import os, random, string
from flask import Flask, render_template, request, flash, session, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
from quote_fun import quote
from functions_for_template import movies_dict, movies, other, key, half_key, top, randoms, recent
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

#Create a MongoDB datebase with hidden login data (with help of python dotenv)
client = MongoClient(os.getenv("LOGIN_DATA"))
app.db = client.Movies

#Titles can't start with this characters(they makes faults in url)
character_list = ["#", ".", ",", "{", "}", "\\", "^", "~",";", "/", "=","£","¤","¥","¦","¨","ª","«"]


#Send quotes to navbar with help of context_processor
@app.context_processor
def context_processor():
    return dict(quote=quote)
    
#Home page where user can recommend a movie
@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == "POST":
        #Use capitalize to get every title with capital first character
        movie = request.form.get("title").capitalize()
        #Prevent to add title starts with strang characters
        if len(movie) > 0 and movie[0] in character_list:
            flash ("Title can't begins with characters as # . , { } ^ ; \ / or ~")
            return render_template("home.html")
        else:
            #If movie title is longer than 25 characters add "..." at the end
            if len(movie) > 25:
                movie = movie[:25] + "..."
            else:
                movie
            #Add movie to datebase if user typed title
                if movie:
                    app.db.movie.insert_one({"movie title": movie})

                    return render_template("thanks.html")
            # Prevent to add en empty data to the datebase
                else:
                    flash("Text field can't be empty. Please write a title.")
                    return render_template("home.html")
    else:
        return render_template("home.html")


#Second page where user can find recommendations made by other users
@app.route('/recommendations/')
def recommendations():
    top_10 = top()
    recent_recommendations = recent()
    random_movie = randoms()

    return render_template("recommendations.html", most_common_movie=top_10, random_movie=random_movie,
                        recent_recommendations=recent_recommendations)
    
    
#A page with all recomendations in alphabethical order
@app.route('/recommendations_all/')
def recommendations_all():
    dictionary_movies_start_with = movies()
    dictionary_movies_other_characters = other()
    key_list = key()
    half_key_list = half_key()
    
    return render_template("all_recommendations.html", movies=dictionary_movies_start_with,
                    others=dictionary_movies_other_characters, key_list=key_list, half_key_list=half_key_list)


#On this page we thanks for the recommendation
@app.route('/thanks')
def thanks():
    return render_template("thanks.html")


#Make pages with list of the movies stated with a specified letter
@app.route('/all_recommendations/<letter>')
def all_letters(letter):
    movies_dictionary = movies_dict()
    return render_template("all.html", movies_dictionary=movies_dictionary)
 


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
