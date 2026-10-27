import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

df = pd.read_csv("movies.csv")
df["overview"] = df["overview"].fillna("")

print(df.shape)
print(df.head(3))
print(df.isnull().sum())

vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(df["overview"])

print(tfidf_matrix.shape)