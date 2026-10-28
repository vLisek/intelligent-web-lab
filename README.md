# Inteligentne Systemy Internetowe

Repozytorium z laboratoriami. Branch: OH.

## Moduł 01: rekomendacje (lab 2 i lab 3)

W tym module zrobiłem dwa silniki rekomendacji filmów, każdy w osobnym folderze
i każdy jako małe API we Flasku.

### Lab 2: content-based (lab2/)

Rekomendacje na podstawie opisów filmów. Z opisów robię macierz TF-IDF, a potem
liczę podobieństwo kosinusowe między filmami. Dla wybranego filmu zwracam te,
które mają najbardziej podobne słownictwo w opisie. Opcjonalnie można filtrować
po gatunku.

Endpoint: `/api/recommend?title=Inception&top_n=2&genre=action`

Przykładowa odpowiedź dla `?title=Inception&top_n=1`:

```json
{
  "count": 1,
  "recommendations": [
    {"genres": "sci-fi|mystery", "rating": 8.0, "score": 0.091, "title": "Blade Runner 2049"}
  ],
  "title": "Inception"
}
```

Błędy: brak `title` lub zły `top_n` (poza 1-10) to 400, nieznany film to 404.

### Lab 3: collaborative filtering (lab3/)

Rekomendacje na podstawie ocen użytkowników, bez czytania opisów filmów. Z
`ratings.csv` robię macierz osoby x filmy, odejmuję od ocen średnią każdej osoby
(centrowanie) i liczę podobieństwo kosinusowe między osobami. Ocenę nieocenionego
filmu przewiduję jako średnią osoby plus ważone odchylenia jej k najbliższych
sąsiadów. Filmy, które osoba już oceniła, nie są polecane.

Endpointy:
- `/api/recommend?user=Ania&k=3&top_n=5` - rekomendacje (k od 1 do 11, domyślnie 3)
- `/api/similar?user=Ania` - najbardziej podobne osoby
- `/api/users` - lista użytkowników

Przykładowa odpowiedź dla `?user=Ania&k=1` (skrócona do jednego filmu):

```json
{
  "count": 4,
  "k": 1,
  "recommendations": [
    {"because": ["Celina"], "predicted": 4.08, "title": "Fight Club"}
  ],
  "user": "Ania"
}
```

Błędy: brak `user` lub zły `k`/`top_n` to 400, nieznany użytkownik to 404 (z listą
znanych użytkowników w odpowiedzi).

### Jak uruchomić

Z głównego folderu repo, w aktywnym środowisku `.venv`:

```
pip install -r lab3/requirements.txt
python lab3/app.py
```

Dla labu 2 analogicznie z folderem `lab2`. Oba serwery używają portu 5000, więc
uruchamiam jeden na raz. Testy labu 3 (z folderu `lab3`):

```
pip install pytest
python -m pytest test_lab03.py -q
```
