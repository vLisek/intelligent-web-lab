import pandas as pd

df = pd.read_csv("movies.csv")
df["overview"] = df["overview"].fillna("")

print(df.shape)
print(df.head(3))
print(df.isnull().sum())