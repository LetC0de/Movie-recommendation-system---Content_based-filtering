# import streamlit as st
# import pandas as pd 
# import requests
# import pickle
# # ================== START: GOOGLE DRIVE PICKLE LOADER ==================

# import os
# import pickle
# import streamlit as st
# import gdown

# #  CHANGE ONLY THIS
# SIMILARITY_FILE_ID = "PASTE_YOUR_FILE_ID_HERE"
# SIMILARITY_PATH = "similarity.pkl"

# #  Download similarity.pkl from Google Drive (only once)
# def download_similarity():
#     if not os.path.exists(SIMILARITY_PATH):
#         url = f"https://drive.google.com/file/d/12qZGIV4ZWxzlaH4W9XJtKzQB7Pz1PoJ3/view?usp=sharing"
#         gdown.download(url, SIMILARITY_PATH, quiet=False)

# #Load pickle safely (cached)
# @st.cache_resource
# def load_similarity():
#     download_similarity()
#     with open(SIMILARITY_PATH, "rb") as f:
#         return pickle.load(f)

# # This is what you will use in your app
# similarity = load_similarity()

# # ================== END: GOOGLE DRIVE PICKLE LOADER ==================




# movies_dict = pickle.load(open("movies_dict.pkl","rb"))
# movies = pd.DataFrame(movies_dict)
# similarity = pickle.load(open("similarity.pkl","rb"))

# def fetch_poster(movie_id):
#     response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id))
#     data = response.json()
    
#     return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


# def recommend(movie):
#     movie_index = movies[movies["title"] == movie].index[0]
#     distances = similarity[movie_index]
#     movies_list = sorted(list(enumerate(distances)) ,reverse=True ,key=lambda x:x[1])[1:6]

#     recommended_movies = []
#     recommended_movie_posters = []
#     for i in movies_list:
#         movie_id = movies.iloc[i[0]].movie_id
#         recommended_movies.append(movies.iloc[i[0]].title)
#         #fetch movie poster from API
#         recommended_movie_posters.append(fetch_poster(movie_id))
#     return recommended_movies,recommended_movie_posters


# st.title("Movie Recommender System")

# selected_movie_name = st.selectbox("Write Movie Name ",movies["title"].values)

# if st.button('Recommend'):
#     # recommendations=recommend(selected_movie_name)
#     # for i in recommendations:
#     #     st.write(i)
#     names,posters = recommend(selected_movie_name)

#     cols = st.columns(5)

#     for i, col in enumerate(cols):
#         with col:
#             st.markdown(
#                 f"<h4 min-height:60px'>{names[i]}</h4>",
#                 unsafe_allow_html=True
#             )
#             st.image(posters[i], use_container_width=True)


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















# ================== GOOGLE DRIVE NUMPY LOADER ==================

import os
import streamlit as st
import gdown
import numpy as np
import pandas as pd
import requests
import pickle

# 🔴 GOOGLE DRIVE FILE ID FOR similarity.npy
SIMILARITY_FILE_ID = "1uVE4oAgL2C12tfYTtPlcOCRvidhkaT__"
SIMILARITY_PATH = "similarity.npy"

# Download similarity.npy only once
def download_similarity():
    if not os.path.exists(SIMILARITY_PATH):
        url = f"https://drive.google.com/uc?id={SIMILARITY_FILE_ID}"
        gdown.download(url, SIMILARITY_PATH, quiet=False)

# Load similarity safely (cached)
@st.cache_resource
def load_similarity():
    download_similarity()
    return np.load(SIMILARITY_PATH)

similarity = load_similarity()

# ================== LOAD MOVIES DATA ==================

movies_dict = pickle.load(open("movies_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

# ================== HELPER FUNCTIONS ==================

def fetch_poster(movie_id):
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}"
        "?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    )
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]

def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters

# ================== STREAMLIT UI ==================

st.title("🎬 Movie Recommender System")

selected_movie_name = st.selectbox(
    "Select a movie",
    movies["title"].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)

    for i, col in enumerate(cols):
        with col:
            st.markdown(
                f"<h4 style='min-height:60px'>{names[i]}</h4>",
                unsafe_allow_html=True
            )
            st.image(posters[i], use_container_width=True)
