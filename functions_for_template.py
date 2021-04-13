import os, string
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

client = MongoClient(os.getenv("LOGIN_DATA"))
db = client.Movies

#Titles can't start with this characters(they makes faults in url)
character_list = ["#", ".", ",", "{", "}", "\\", "^", "~",";", "/", "=","£","¤","¥","¦","¨","ª","«"]

movie_list = []
movies = db.movie.find({})
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

#Make a list with all first letters and list with all first characters in titles (for buttons)
key_list = list(dictionary_movies_start_with.keys()) + list(dictionary_movies_other_characters.keys())
half_key_list = int(len(key_list)/2)



def movies_dict():
    movies_dictionary = {**dictionary_movies_other_characters, **dictionary_movies_start_with}
    return movies_dictionary 

def movies():
    dictionary_movies_start_with
    return dictionary_movies_start_with

def other():
    dictionary_movies_other_characters
    return dictionary_movies_other_characters

def characters():
    character_list
    return character_list

def key():
    key_list
    return key_list

def half_key():
    half_key_list
    return half_key_list

 