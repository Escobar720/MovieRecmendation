# # This is a sample Python script.
#
# # Press Shift+F10 to execute it or replace it with your code.
# # Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
#
#
# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')
#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/
from flask import Flask , request, render_template , request
import streamlit as st
import pickle
import requests
import pandas as pd
from patsy import dmatrices

movies = pickle.load(open('model/movies_list.pkl', 'rb'))
similarity = pickle.load(open('model/similarity_list.pkl', 'rb'))

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmbd.org/t/p/w500/" + poster_path
    return full_path



def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse= True, key = lambda x: x[1])
    recommend_movies_name = []
    recommend_movies_poster = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movies_poster.append(fetch_poster(movie_id))
        recommend_movies_name.append(movies.iloc[i[0]].title)


    return recommend_movies_name, recommend_movies_poster


app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/Movies")
def movie():
    return render_template('Movies.html')

@app.route("/index2" , methods = ['GET' , 'POST'])
def recommend_movie():
    movie_list = movies['title'].values
    recommend_movies_name = []
    recommend_movies_poster = []
    status  = False
    if request.method == "POST":
        try:
            if request.form:
                movies_name = request.form['movies']
                print(movies_name)
                recommend_movies_name , recommend_movies_poster = recommend(movies_name)
                status = True
                print(recommend_movies_name)
                print(recommend_movies_poster)

            return  render_template('index2.html' , movies_name = recommend_movies_name, poster = recommend_movies_poster, movie_list = movie_list , status = status)


        except Exception as e:
            error = {'error' : e}
            return render_template('index2.html', error = error,   movie_list = movie_list , status = status)
        
    else:
        return render_template("index2.html",  movie_list = movie_list, status = status)




app.run(debug=True)