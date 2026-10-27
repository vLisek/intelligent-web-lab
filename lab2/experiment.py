from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

HERE = Path(__file__).parent


def rank(csv_name, title, top_n=5):
    df = pd.read_csv(HERE / csv_name)
    df["overview"] = df["overview"].fillna("")
    X = TfidfVectorizer(stop_words="english").fit_transform(df["overview"])
    sim = cosine_similarity(X)
    idx = df.index[df["title"] == title][0]
    scores = sorted(enumerate(sim[idx]), key=lambda x: x[1], reverse=True)
    return [(df["title"][i], round(float(s), 3)) for i, s in scores if i != idx][:top_n]


for t in ["Her", "Interstellar"]:
    print(t, "PRZED:", rank("movies.csv", t))
    print(t, "PO:   ", rank("movies_test.csv", t))
    print()