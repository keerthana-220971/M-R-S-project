import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies = pd.read_csv("movies.csv")

movies['genres'] = movies['genres'].fillna('')

tfidf = TfidfVectorizer(stop_words='english')

tfidf_matrix = tfidf.fit_transform(movies['genres'])

cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

movies = movies.reset_index()

def recommend(movie_title):

    idx = movies[movies['title'] == movie_title].index[0]

    similarity_scores = list(enumerate(cosine_sim[idx]))

    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    similarity_scores = similarity_scores[1:11]

    movie_indices = [i[0] for i in similarity_scores]

    return movies['title'].iloc[movie_indices]