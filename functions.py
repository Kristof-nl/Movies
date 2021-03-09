def list_movies_start_with(letter):
    lst = []
    for movie in alphabethical_movie_list:
        if movie.startswith(chr(letter)):
            lst.append(movie)
    return lst
