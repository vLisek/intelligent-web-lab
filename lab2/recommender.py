from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ścieżka do CSV liczona względem tego pliku, a nie folderu, z którego uruchamiasz skrypt
df = pd.read_csv(Path(__file__).parent / "movies.csv")
df["overview"] = df["overview"].fillna("")

vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(df["overview"])

sim_matrix = cosine_similarity(tfidf_matrix)  # 24 x 24, każdy film z każdym


def recommend(title, top_n=5):
    match = df[df["title"].str.lower() == title.lower()]
    if match.empty:
        return None
    idx = match.index[0]
    scores = sorted(enumerate(sim_matrix[idx]), key=lambda x: x[1], reverse=True)
    return [
        {
            "title": df["title"][i],
            "genres": df["genres"][i],
            "rating": round(float(df["rating"][i]), 1),
            "score": round(float(s), 3),
        }
        for i, s in scores
        if i != idx
    ][:top_n]


if __name__ == "__main__":
    print(df.shape)
    print(tfidf_matrix.shape)
    print(sim_matrix.shape)
    print(recommend("Inception"))
    print(recommend("The Matrix", top_n=3))