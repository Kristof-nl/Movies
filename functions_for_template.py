import os, string, random
from pymongo import MongoClient
from statistics import multimode
from dotenv import load_dotenv
load_dotenv()

client = MongoClient(os.getenv("LOGIN_DATA"))
db = client.Movies


#Get data from datebase
def datebase():
    movie_list = []
    movies = db.movie.find({})
    for movie in movies:
        movie_list.append(movie['movie title'])

    return movie_list

        
def movies():
    #Call datebase to refresh data in route
    movie_list = datebase()
    #Make a dictionary with all movies for all_recommendations page
    #Delete all repeats by creating a set
    movie_set = set(movie_list)
    alphabethical_movie_list = sorted(movie_set)

    #Dictionary is apart to shown first movies begins with letters from alphabet
    dictionary_movies_start_with = {'A':[], 'B':[], 'C':[], 'D':[], 'E':[], 'F':[], 'G':[], 'H':[], 'I':[], 'J':[],
    'K':[], 'L':[], 'M':[], 'N':[], 'O':[], 'P':[], 'Q':[], 'R':[], 'S':[], 'T':[], 'U':[], 'V':[], 'W':[], 'X':[],
    'Y':[], 'Z':[]}

    # Create list with alphabet
    alphabet = list(string.ascii_uppercase)
    for movie in alphabethical_movie_list:
    #Add movies starts with letter from alphabet
        if movie[0] in alphabet:
            dictionary_movies_start_with[movie[0]].append(movie)
    
    return dictionary_movies_start_with


def other():
    #Call datebase to refresh data in route
    movie_list = datebase()
    #Make a dictionary with all movies for all_recommendations page
    #Delete all repeats by creating a set
    movie_set = set(movie_list)
    alphabethical_movie_list = sorted(movie_set)

    #Dictionary with movies begins with characters without alphabet
    dictionary_movies_other_characters = {}

    #List with alphabet letters to add movies starts with other characters 
    alphabet = list(string.ascii_uppercase)
    for movie in alphabethical_movie_list:
        if movie[0] not in dictionary_movies_other_characters.keys() and movie[0] not in alphabet:
            dictionary_movies_other_characters.update({movie[0]:[]})

    #Add movie to dictionary_movies_other_characters if it starts with character outside the alphabet
    for movie in alphabethical_movie_list:
        if movie[0] in dictionary_movies_other_characters:
            dictionary_movies_other_characters[movie[0]].append(movie)

    return dictionary_movies_other_characters    
                       

def movies_dict():
    #Call datebase to refresh data in route
    movie_list = datebase()
    #Make a new dictionary with all letters and characters
    dictionary_movies_other_characters = other()
    dictionary_movies_start_with = movies()
    movies_dictionary = {**dictionary_movies_other_characters, **dictionary_movies_start_with}

    return movies_dictionary 


#Make a list with all first letters and list with all first characters in titles (for buttons)
def key():
    #Call datebase to refresh data in route
    movie_list = datebase()
    dictionary_movies_other_characters = other()
    dictionary_movies_start_with = movies()
    key_list = list(dictionary_movies_start_with.keys()) + list(dictionary_movies_other_characters.keys())

    return key_list

# For buttons
def half_key():
    #Call datebase to refresh data in route
    movie_list = datebase()
    key_list = key()
    half_key_list = int(len(key_list)/2)

    return half_key_list

#Most common recommendations
def top():
    #Call datebase to refresh data in route
    movie_list = datebase()
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
    return top_10


#Random recommedation
def randoms():
    #Call datebase to refresh data in route
    movie_list = datebase()
    random_movie = random.choice(movie_list)
    return random_movie


#Recent recommendations
def recent():
    #Call datebase to refresh data in route
    movie_list = datebase()
    recent_recommendations = []
    temporary_recent_list = movie_list[:]
    # If are 10 or more movies in datebase
    if len(set(movie_list)) >= 10:
        while len(recent_recommendations) != 10:
            recent_movie = temporary_recent_list.pop()
            if recent_movie not in recent_recommendations:
                recent_recommendations.append(recent_movie)
    else:
        #If are less than 10 movies in datebase
        while len(recent_recommendations) != len(set(movie_list)):
            recent_movie = temporary_recent_list.pop()
            if recent_movie not in recent_recommendations:
                recent_recommendations.append(recent_movie)
    return recent_recommendations

