import os, random, string
from flask import Flask, render_template, request, flash, session, url_for
from pymongo import MongoClient
from statistics import multimode
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

#Create a MongoDB datebase with hidden login data (with help of python dotenv)
client = MongoClient(os.getenv("LOGIN_DATA"))
app.db = client.Movies

#Titles can't start with this characters(they makes faults in url)
character_list = ["#", ".", ",", "{", "}", "\\", "^", "~",";", "/", "=","£","¤","¥","¦","¨","ª","«"]


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
    movie_list = []
    movies = app.db.movie.find({})
    for movie in movies:
        movie_list.append(movie['movie title'])

    if movie_list:
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
    movie_list = []
    movies = app.db.movie.find({})
    for movie in movies:
        movie_list.append(movie['movie title'])

    #Make a dictionary with all movies for all_recommendations page
    #Delete all repeats by creating a set
    movie_set = set(movie_list)
    alphabethical_movie_list = sorted(movie_set)

    #Dictionary is apart to shown first movies begins with letters from alphabet
    dictionary_movies_start_with = {'A':[], 'B':[], 'C':[], 'D':[], 'E':[], 'F':[], 'G':[], 'H':[], 'I':[], 'J':[],
    'K':[], 'L':[], 'M':[], 'N':[], 'O':[], 'P':[], 'Q':[], 'R':[], 'S':[], 'T':[], 'U':[], 'V':[], 'W':[], 'X':[],
    'Y':[], 'Z':[]}

    #Dictionary with movies begins with characters without alphabet
    dictionary_movies_other_characters = {}

    #List with alphabet letters to add movies starts with other characters 
    alphabet = list(string.ascii_uppercase)
    for movie in alphabethical_movie_list:
        #Add movies starts with letter from alphabet
        if movie[0] in alphabet:
            dictionary_movies_start_with[movie[0]].append(movie)
        #Create keys for dictionary_movies_other_characters
        else:
            if movie[0] not in dictionary_movies_other_characters.keys():
                dictionary_movies_other_characters.update({movie[0]:[]})
    #Add movie to dictionary_movies_other_characters if it starts with character outside the alphabet
    for movie in alphabethical_movie_list:
        if movie[0] in dictionary_movies_other_characters:
            dictionary_movies_other_characters[movie[0]].append(movie)

    #Make a new dictionary with all letters and characters
    movies_dictionary = {**dictionary_movies_other_characters, **dictionary_movies_start_with}
    session['dictionary'] = movies_dictionary

    #Make a list with all first letters and list with all first characters in titles (for buttons)
    key_list = list(dictionary_movies_start_with.keys()) + list(dictionary_movies_other_characters.keys())
    half_key_list = int(len(key_list)/2)
    print(type(half_key_list))
    print(half_key_list)


    return render_template("all_recommendations.html", movies=dictionary_movies_start_with,
                    others=dictionary_movies_other_characters, character_list=character_list,
                    key_list=key_list, half_key_list=half_key_list)


#On this page we thanks for the recommendation
@app.route('/thanks')
def thanks():
    return render_template("thanks.html")


#Make pages with list of the movies stated with a specified letter
@app.route('/all_recommendations/<letter>')
def all_letters(letter):
    movies_dictionary = session.get('dictionary', None)
    return render_template("all.html", movies=movies_dictionary[letter])
 

if __name__ == "__main__":
    app.run(debug=True)
