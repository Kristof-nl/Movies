import os, random, string
from flask import Flask, render_template, request
from pymongo import MongoClient
from statistics import multimode
from dotenv import load_dotenv
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

#Make a dictionary with all movies for all_recommendations page
#Delete all repeats by creating a set
movie_set = set(movie_list)
alphabethical_movie_list = sorted(movie_set)

dictionary_movies_start_with = {'A':[], 'B':[], 'C':[], 'D':[], 'E':[], 'F':[], 'G':[], 'H':[], 'I':[], 'J':[],
'K':[], 'L':[], 'M':[], 'N':[], 'O':[], 'P':[], 'Q':[], 'R':[], 'S':[], 'T':[], 'U':[], 'V':[], 'W':[], 'X':[],
'Y':[], 'Z':[]}


list_movies_other = []


#List with alphabet letters to add movies starts with other characters
alphabet = list(string.ascii_uppercase)


for movie in alphabethical_movie_list:
    #Add movies starts with letter from alphabet
    if movie[0] in alphabet:
        dictionary_movies_start_with[movie[0]].append(movie)
    #Add movie to list_movies_other if it starts with character outside the alphabet
    else:
        list_movies_other.append(movie)
        

#Home page where user can recommend a movie
@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == "POST":
        #Use capitalize to get every title with capital first character
        movie = request.form.get("title").capitalize()
        #If movie title is longer than 30 characters add "..." at the end
        if len(movie) > 30:
            movie = movie + "..."
        else:
            pass
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
    return render_template("all_recommendations.html", movies=dictionary_movies_start_with, others=list_movies_other)


#On this page we thanks for the recommendation
@app.route('/thanks')
def thanks():
    return render_template("thanks.html")


#Make pages with list of the movies stated with a specified letter
@app.route('/all_recommendations/A')
def a():
    return render_template("allrecomendations/a.html", movies=dictionary_movies_start_with['A'])
        
@app.route('/all_recommendations/B')
def b():
    return render_template("allrecomendations/b.html", movies=dictionary_movies_start_with['B'])

@app.route('/all_recommendations/C')
def c():
    return render_template("allrecomendations/c.html", movies=dictionary_movies_start_with['C'])  

@app.route('/all_recommendations/D')
def d():
    return render_template("allrecomendations/d.html", movies=dictionary_movies_start_with['D']) 

@app.route('/all_recommendations/E')
def e():
    return render_template("allrecomendations/a.html", movies=dictionary_movies_start_with['E'])

@app.route('/all_recommendations/F')
def f():
    return render_template("allrecomendations/f.html", movies=dictionary_movies_start_with['F'])

@app.route('/all_recommendations/G')
def g():
    return render_template("allrecomendations/g.html", movies=dictionary_movies_start_with['G'])

@app.route('/all_recommendations/H')
def h():
    return render_template("allrecomendations/h.html", movies=dictionary_movies_start_with['H'])

@app.route('/all_recommendations/I')
def i():
    return render_template("allrecomendations/i.html", movies=dictionary_movies_start_with['I'])

@app.route('/all_recommendations/J')
def j():
    return render_template("allrecomendations/j.html", movies=dictionary_movies_start_with['J'])

@app.route('/all_recommendations/K')
def k():
    return render_template("allrecomendations/k.html", movies=dictionary_movies_start_with['K'])

@app.route('/all_recommendations/L')
def l():
    return render_template("allrecomendations/l.html", movies=dictionary_movies_start_with['L'])

@app.route('/all_recommendations/M')
def m():
    return render_template("allrecomendations/m.html", movies=dictionary_movies_start_with['M'])

@app.route('/all_recommendations/N')
def n():
    return render_template("allrecomendations/n.html", movies=dictionary_movies_start_with['N'])

@app.route('/all_recommendations/O')
def o():
    return render_template("allrecomendations/o.html", movies=dictionary_movies_start_with['O'])

@app.route('/all_recommendations/P')
def p():
    return render_template("allrecomendations/p.html", movies=dictionary_movies_start_with['P'])

@app.route('/all_recommendations/Q')
def q():
    return render_template("allrecomendations/q.html", movies=dictionary_movies_start_with['Q'])

@app.route('/all_recommendations/R')
def r():
    return render_template("allrecomendations/r.html", movies=dictionary_movies_start_with['R'])

@app.route('/all_recommendations/S')
def s():
    return render_template("allrecomendations/s.html", movies=dictionary_movies_start_with['S'])

@app.route('/all_recommendations/T')
def t():
    return render_template("allrecomendations/t.html", movies=dictionary_movies_start_with['T'])

@app.route('/all_recommendations/U')
def u():
    return render_template("allrecomendations/u.html", movies=dictionary_movies_start_with['U'])

@app.route('/all_recommendations/V')
def v():
    return render_template("allrecomendations/v.html", movies=dictionary_movies_start_with['V'])

@app.route('/all_recommendations/W')
def w():
    return render_template("allrecomendations/w.html", movies=dictionary_movies_start_with['W'])

@app.route('/all_recommendations/X')
def x():
    return render_template("allrecomendations/x.html", movies=dictionary_movies_start_with['X'])

@app.route('/all_recommendations/Y')
def y():
    return render_template("allrecomendations/y.html", movies=dictionary_movies_start_with['Y'])

@app.route('/all_recommendations/Z')
def z():
    return render_template("allrecomendations/z.html", movies=dictionary_movies_start_with['Z'])

@app.route('/all_recommendations/Other')
def other():
    return render_template("allrecomendations/other.html", movies=list_movies_other)


if __name__ == "__main__":
    app.run(debug=True)