import os
from flask import Flask, render_template, request
from pymongo import MongoClient
from statistics import mode
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)

#Create a MongoDB datebase with hidden password (with help of python dotenv)
client = MongoClient("mongodb+srv://Krzysztof_nl:"+os.getenv("PASSWORD")+"@cluster0.dsf4q.mongodb.net/test")
app.db = client.Movies

movie_list = []
alphabethical_movie_list = sorted(movie_list)
movies = app.db.movie.find({})
for movie in movies:
    movie_list.append(movie['movie title'])

#Home page where user can recommend a movie
@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == "POST":
        movie = request.form.get("title")
        #Add movie to datebase if user typed title
        if movie:
            app.db.movie.insert_one({"movie title": movie})
            return render_template("thanks.html")
        # Prevent to add en empty data to the datebase
        else:
            return render_template("home.html")
    else:
        return render_template("home.html")

#Second page where user can find recommendations made by other users
@app.route('/recommendations/')
def recommendations():
    #Most common recomendation
    top_5 = []
    temporary_list = movie_list[:]
    for i in range(5):
        most_common_movie = mode(movie_list)

    return render_template("recommendations.html", most_common_movie=most_common_movie)

#A page with all recomendations in alphabethical order
@app.route('/recommendations_all/')
def recommendations_all():
    #Delete all repeats by creating a set
    movie_set = set(movie_list)
    alphabethical_movie_list = sorted(movie_set)
    return render_template("all_recommendations.html", movies=alphabethical_movie_list)


#On this page we thanks for the recommendation
@app.route('/thanks')
def thanks():
    return render_template("thanks.html")




if __name__ == "__main__":
    app.run(debug=True)