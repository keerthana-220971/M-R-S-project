from dotenv import load_dotenv
import os
import streamlit as st
import pandas as pd
import requests
from recommender import recommend

load_dotenv()
API_KEY = os.getenv("TMDB-API_KEY")

movies = pd.read_csv("movies.csv")


def fetch_poster(movie_name):
    try:
        url = "https://api.themoviedb.org/3/search/movie"
        params = {
            "api_key": API_KEY,
            "query": movie_name
        }

        response = requests.get(url, params=params)
        data = response.json()

        if data["results"]:
            poster_path = data["results"][0].get("poster_path")

            if poster_path:
                return "https://image.tmdb.org/t/p/w500" + poster_path

        return "https://via.placeholder.com/300x450?text=No+Poster"

    except Exception as e:
        return "https://via.placeholder.com/300x450?text=Error"

st.title("🎬 AI Movie Recommendation System")

movie_name = st.selectbox("Select a Movie", movies['title'])

if st.button("Recommend"):

    recommendations = recommend(movie_name)

    st.subheader("Recommended Movies")

    cols = st.columns(5)

    for i, movie in enumerate(recommendations):

        poster = fetch_poster(movie)

        with cols[i % 5]:
            if poster:
                st.image(poster)
            st.write(movie)