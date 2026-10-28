from pathlib import Path

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

HERE = Path(__file__).parent
TARGET = "Ania"      # dla kogo liczymy rekomendacje
CHANGED = "Celina"   # czyja ocena została zmieniona


def build(csv_name):
    df = pd.read_csv(HERE / csv_name)
    matrix = df.pivot_table(index="user", columns="title", values="rating")
    means = matrix.mean(axis=1)
    centered = matrix.sub(means, axis=0).fillna(0)
    sim = pd.DataFrame(cosine_similarity(centered), index=matrix.index, columns=matrix.index)
    return matrix, means, sim


def recommend(matrix, means, sim, user, k=3, top_n=5):
    neighbors = sim[user].drop(user).sort_values(ascending=False).head(k)
    scores = {}
    for movie in matrix.columns:
        if not pd.isna(matrix.loc[user, movie]):
            continue
        num, den = 0.0, 0.0
        for other, w in neighbors.items():
            r = matrix.loc[other, movie]
            if not pd.isna(r):
                num += w * (r - means[other])
                den += abs(w)
        if den > 0:
            scores[movie] = max(1.0, min(5.0, means[user] + num / den))
    best = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
    return [(t, round(float(s), 2)) for t, s in best]


for name in ["ratings.csv", "ratings_test.csv"]:
    matrix, means, sim = build(name)
    print("=====", name)
    print("srednia", CHANGED, ":", round(float(means[CHANGED]), 3))
    print("srednia", TARGET, ":", round(float(means[TARGET]), 3))
    print("sasiedzi", TARGET, ":", sim[TARGET].drop(TARGET).sort_values(ascending=False).head(3).round(3).to_dict())
    print("rekomendacje (k=3):", recommend(matrix, means, sim, TARGET))
    print()