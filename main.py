# import pandas library
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
import numpy as np


class RecSystem:

    def __init__(self):

        # Users and Ratings
        self.data_users = pd.read_csv('ml-latest-small/ratings.csv')

        # Movie titles
        self.movie_titles = pd.read_csv('ml-latest-small/movies.csv')

        self.data = pd.merge(self.data_users, self.movie_titles, on='movieId')

    def get_movie_title(self, movie_input, top_rated_movies):

        matching = []
        for i in top_rated_movies['title']:
            if movie_input in i.lower():
                matching.append(i)

        for i in matching:
            print(i)
        return matching



    def rec_me_a_movie(self, movie_input):
        data = self.data
        data.groupby('title')['rating'].mean().sort_values(ascending=False).head()

        # creating dataframe with 'rating' count values
        ratings = pd.DataFrame(data.groupby('title')['rating'].mean())
        ratings['num of ratings'] = pd.DataFrame(data.groupby('title')['rating'].count())

        # Sorting values according to the 'num of rating column'
        moviemat = data.pivot_table(index='userId', columns='title', values='rating')
        for i in moviemat:
            moviemat[i] = moviemat[i].fillna(moviemat[i].mean())

        top_rated_movies = (ratings.sort_values('num of ratings', ascending=False)).reset_index(level=['title'])
        movie_title = self.get_movie_title(movie_input, top_rated_movies)
        movie_user_ratings = moviemat[ movie_title[0]]

        similar_to_input_movie = moviemat.corrwith(movie_user_ratings)
        corr_movie = pd.DataFrame(similar_to_input_movie, columns=['Correlation'])
        corr_movie.dropna(inplace=True)
        corr_movie.sort_values('Correlation', ascending=False).head(10)
        corr_movie = corr_movie.join(ratings['num of ratings'])
        result = corr_movie[corr_movie['num of ratings'] > 100].sort_values('Correlation', ascending=False).head()
        r = result.reset_index(level=['title'])
        return r['title']

################################### MAIN #################################################

if __name__ == "__main__":

    movie_object = RecSystem()

    # Get argument and search in list of movie titles and fetch movie
    movie_input = input("Search for a movie: ")

    # get_movie_title = movie_object.get_movie_title(movie_input.lower())
    rec_movies = []
    rec_movies = movie_object.rec_me_a_movie(movie_input.lower())

    for i in rec_movies:
        print(i)

    # if rec_movies:
    #     for i in rec_movies:
    #         print(i)
    # else:
    #     print("Sorry, couldn't find anything :(")
