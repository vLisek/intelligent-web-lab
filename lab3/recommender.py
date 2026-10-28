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

if __name__ == "__main__":
    print(matrix.shape)
    print(means.round(2))
    print(sim.shape)
    print(sim["Ania"].drop("Ania").sort_values(ascending=False).round(3))