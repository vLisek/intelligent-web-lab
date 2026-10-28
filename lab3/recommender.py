from pathlib import Path

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv(Path(__file__).parent / "ratings.csv")
matrix = df.pivot_table(index="user", columns="title", values="rating")

means = matrix.mean(axis=1)
centered = matrix.sub(means, axis=0).fillna(0)

sim = pd.DataFrame(
    cosine_similarity(centered),
    index=matrix.index,
    columns=matrix.index,
)

def recommend(user, top_n=5, k=3):
    if user not in matrix.index:
        return None

    neighbors = sim[user].drop(user).sort_values(ascending=False).head(k)

    scores = {}
    for movie in matrix.columns:
        if not pd.isna(matrix.loc[user, movie]):
            continue  # ten film Ania już oceniła, nie polecamy go
        num, den = 0.0, 0.0
        for other, w in neighbors.items():
            r = matrix.loc[other, movie]
            if not pd.isna(r):
                num += w * (r - means[other])
                den += abs(w)
        if den > 0:
            scores[movie] = max(1.0, min(5.0, means[user] + num / den))

    best = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
    return [
        {
            "title": t,
            "predicted": round(float(s), 2),
            "because": [
                o for o, w in neighbors.items()
                if w != 0 and not pd.isna(matrix.loc[o, t])
            ],
        }
        for t, s in best
    ]


if __name__ == "__main__":
    print(recommend("Ania"))
    print(recommend("Ania", top_n=3, k=1))
    print(recommend("Nikt"))

if __name__ == "__main__":
    print(matrix.shape)
    print(means.round(2))
    print(sim.shape)
    print(sim["Ania"].drop("Ania").sort_values(ascending=False).round(3))

