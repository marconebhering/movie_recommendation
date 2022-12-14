import pandas as pd
import streamlit as st
import pickle
import requests

st.set_page_config(page_title = "Sistema de Recomendação de Filmes")

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=020b311fe0559698373a16008dc6a672&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for x in movies_list:
        movie_id = movies.iloc[x[0]].movie_id
        recommended_movies.append(movies.iloc[x[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))
st.title('Sistema de Recomendação de Filmes')

selected_movie_name = st.selectbox(
    'Escolha um filme que você gosta:',
    movies['title'].values
)

if st.button('Recomendar'):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(posters[0], caption=names[0])
    with col2:
        st.image(posters[1], caption=names[1])
    with col3:
        st.image(posters[2], caption=names[2])
    with col4:
        st.image(posters[3], caption=names[3])
    with col5:
        st.image(posters[4], caption=names[4])

