import streamlit as st
import pickle
import pandas as pd
import requests

api_key = '8265bd1679663a7ea12ac168da84d2e8'

def recommend(movie):
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_similar = sorted(enumerate(distances), key=lambda x: x[1], reverse=True)[1:6]
    
    recommended_movies = []
    recommended_movies_posters = []
    
    for i in movies_similar:
        #print(movies_list['title'][i[0]])
        recommended_movies.append(movies_list['title'][i[0]])
        
        # Fetch movie posters from API
        recommended_movies_posters.append(fetch_poster(movies_list['movie_id'][i[0]]))
    
    return recommended_movies, recommended_movies_posters

def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}')
    data = response.json()
    
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

movies_list = pickle.load(open('movies_dict.pkl', 'rb'))

movies_list = pd.DataFrame(movies_list)

# similarity_matrix
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title("ShowBox")

# Select Box

selected_movie = st.selectbox('Select a movie', movies_list['title'].values)

# Recommed Button

if st.button('Recommend'):
    names,posters = recommend(selected_movie)
    
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])
        
    with col2:
        st.text(names[1])
        st.image(posters[1])
        
    with col3:
        st.text(names[2])
        st.image(posters[2])
        
    with col4:
        st.text(names[3])
        st.image(posters[3])
    
    with col5:
        st.text(names[4])
        st.image(posters[4])
