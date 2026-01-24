import streamlit as st
import pandas as pd 
import requests
import pickle

movies_dict = pickle.load(open("movies_dict.pkl","rb"))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open("similarity.pkl","rb"))

def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id))
    data = response.json()
    
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)) ,reverse=True ,key=lambda x:x[1])[1:6]

    recommended_movies = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        #fetch movie poster from API
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movie_posters


st.title("Movie Recommender System")

selected_movie_name = st.selectbox("Write Movie Name ",movies["title"].values)

if st.button('Recommend'):
    # recommendations=recommend(selected_movie_name)
    # for i in recommendations:
    #     st.write(i)
    names,posters = recommend(selected_movie_name)

    cols = st.columns(5)

    for i, col in enumerate(cols):
        with col:
            st.markdown(
                f"<h4 min-height:60px'>{names[i]}</h4>",
                unsafe_allow_html=True
            )
            st.image(posters[i], use_container_width=True)


    # col1,col2,col3,col4,col5 = st.columns(5)
    # with col1:
    #     st.header(names[0])
    #     st.image(posters[0])
    # with col2:
    #     st.header(names[1])
    #     st.image(posters[1])
    # with col3:
    #     st.header(names[2])
    #     st.image(posters[2])
    # with col4:
    #     st.header(names[3])
    #     st.image(posters[3])
    # with col5:
    #     st.header(names[4])
    #     st.image(posters[4])

