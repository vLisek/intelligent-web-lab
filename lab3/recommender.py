from pathlib import Path

import pandas as pd

df = pd.read_csv(Path(__file__).parent / "ratings.csv")

matrix = df.pivot_table(index="user", columns="title", values="rating")

if __name__ == "__main__":
    print(df.shape)
    print(matrix.shape)
    print("oceny w macierzy:", matrix.notna().sum().sum())
    print("braki (NaN):", matrix.isna().sum().sum())
    print(matrix.iloc[:3, :5])