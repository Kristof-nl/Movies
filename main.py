import os, random
from flask import Flask, render_template, request
from pymongo import MongoClient
from statistics import multimode
from dotenv import load_dotenv

from functions import list_movies_start_with
load_dotenv()


app = Flask(__name__)

#Create a MongoDB datebase with hidden login data (with help of python dotenv)
client = MongoClient(os.getenv("LOGIN_DATA"))
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
        # Use capitalize to get every title with capital first character
        movie = request.form.get("title").capitalize()
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
    #Random recommedation
    random_movie = random.choice(movie_list)
    #Recent recommendations
    recent_recommendations = []
    temporary_recent_list = movie_list[:]
    # If are 10 or more movies in datebase
    if len(set(movie_list)) >= 10:
        while len(recent_recommendations) != 10:
            recent_movie = temporary_recent_list.pop()
            if recent_movie not in recent_recommendations:
                recent_recommendations.append(recent_movie)
        
    else:
        # If are less than 10 movies in datebase
        while len(recent_recommendations) != len(set(movie_list)):
            recent_movie = temporary_recent_list.pop()
            if recent_movie not in recent_recommendations:
                recent_recommendations.append(recent_movie)
    #Most common recommendations
    top_10 = []
    temporary_list = movie_list[:]
    #Check of temporary_list have more positions than temporary_set. If yes that means that at least
    #one movie have more recommendations than other movies
    temporary_set = set(temporary_list)
    #Check of there is at least on title with more than on recommendation
    if len(temporary_list) != len(list(temporary_set)):
        if len(temporary_set) >= 10:
            while len(top_10) !=10:
                if multimode(temporary_list):
                    # There can be more than one movie with the same number of recommendations
                    for movie in multimode(temporary_list):
                        number_of_recommendations = 0
                        #Delete all accourances from temporary_list to find another most common occurance
                        while movie in temporary_list:
                            number_of_recommendations += 1
                            temporary_list.remove(movie)
                        top_10.append([movie, number_of_recommendations])
                        #Solve problem if there are for exemple all 9 movies in top_10 and multimode gives
                        #2 or more movies to add
                        if len(top_10) == 10:
                            break

        else:
            #If there is less than 10 movies in the datebase:
            while len(top_10) !=len(temporary_set):
                if multimode(temporary_list):
                    for movie in multimode(temporary_list):
                        number_of_recommendations = 0
                        #Delete all accourances from temporary_list to find another most common occurance
                        while movie in temporary_list:
                            number_of_recommendations += 1
                            temporary_list.remove(movie)
                        top_10.append([movie, number_of_recommendations])
                        

        return render_template("recommendations.html", most_common_movie=top_10, random_movie=random_movie,
                            recent_recommendations=recent_recommendations)

    else:
        return render_template("recommendations.html")


#A page with all recomendations in alphabethical order
@app.route('/recommendations_all/')
def recommendations_all():
    #Delete all repeats by creating a set
    movie_set = set(movie_list)
    alphabethical_movie_list = sorted(movie_set)
    #List with list movie startswith letters from alphabet

    def list_movies_start_with(letter):
        lst = []
        for movie in alphabethical_movie_list:
            if movie.startswith(chr(letter)):
                lst.append(movie)
            return lst


    startswith_list = []
    for i in range(24):
        letter = 65
        x = list_movies_start_with(letter)
        startswith_list.append(x)
        letter += 1

    return render_template("all_recommendations.html", movies=startswith_list)


#On this page we thanks for the recommendation
@app.route('/thanks')
def thanks():
    return render_template("thanks.html")



    
if __name__ == "__main__":
    app.run(debug=True)