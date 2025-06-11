from http.client import responses

import streamlit as st
import pickle
import pandas as pd
import requests

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('https://', adapter)


def fetch_poster(movie_id):
    response = session.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=e65d08c9190dc28fc026e603e39abca1',
        timeout=5
    )

    data = response.json()
    return  "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
  movie_index = movies[ movies['title']==movie].index[0]
  distance = cosine_similarity[movie_index]
  movie_list = sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[1])[1:6]
  recommend_movies = []
  recommend_movies_poster = []

  for i in movie_list:
    movie_id = movies.iloc[i[0]].movie_id
    recommend_movies.append(movies.iloc[i[0]].title)
    # fetch movie poster
    recommend_movies_poster.append(fetch_poster(movie_id))
  return recommend_movies,recommend_movies_poster

cosine_similarity = pickle.load(open("similarity.pkl",'rb'))
movie_dict = pickle.load(open("movies_dict.pkl",'rb'))
movies = pd.DataFrame(movie_dict)
st.title("Movie recommender system")

Selected_movie_name = st.selectbox(
    "How would you like to be contacted?",
    movies['title'].values
)
if st.button("Recommend"):
    names,posters =recommend(Selected_movie_name)

# st.write("You can select from the table:", movies['title'])

    col1, col2, col3 ,col4, col5= st.columns(5)


    with col1:
        st.header(names[0])
        st.image(posters[0])

    with col2:
        st.header(names[1])
        st.image(posters[1])

    with col3:
        st.header(names[1])
        st.image(posters[1])

    with col4:
        st.header(names[3])
        st.image(posters[3])

    with col5:
        st.header(names[4])
        st.image(posters[4])
