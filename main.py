import os
from flask import Flask, render_template, request
from pymongo import MongoClient
from statistics import multimode
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)

#Create a MongoDB datebase with hidden password (with help of python dotenv)
client = MongoClient("mongodb+srv://Krzysztof_nl:"+os.getenv("PASSWORD")+"@cluster0.dsf4q.mongodb.net/test")
app.db = client.Movies

#Making a list to get leter a list of unique titles by changint list to a set
movie_list = []
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
            movie_list.append(movie)
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
    #Check of temporary_list have more positions than temporary_set. If yes that means that at least
    #one movie have more than one recommendation
    temporary_set = set(temporary_list)
    for i in range(5):
        if len(temporary_list) != len(list(temporary_set)):
            #Try of the only one title is most common
                if multimode(movie_list):
                    most_common_movie = multimode(movie_list)
                return render_template("recommendations.html", most_common_movie=most_common_movie)

        else:
            return render_template("recommendations.html")


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


print(movie_list)
temporary_list = movie_list[:]
#temporary_set = set(temporary_list)
#print(temporary_list)
#print(list(temporary_set))




if __name__ == "__main__":
    app.run(debug=True)