# Projekt Big Data – Szablon Bazowy

## Cel projektu
Celem tego projektu jest pokazanie pełnego przepływu pracy na dużych danych: od przetwarzania danych w modelu **MapReduce**, przez **eksplorację danych**, aż po **wizualizację wyników**. Ten szablon daje podstawy, które można rozbudować o własny temat i większe zbiory danych.

## Struktura projektu
src/
mapreduce_engine.py
jobs/
word_count.py
transactions_agg.py
imdb_genre_stats.py
imdb_year_stats.py
imdb_ingest.py
imdb_clustering.py
visualize_imdb.py
eda.py
visualize.py

data/
transactions_sample.csv
imdb.csv

tests/
## Instalacja

```bash
pip install -r requirements.txt
pip install -r requirements.txt


## Przykłady użycia MapReduce

# Liczenie słów (Word Count)
python src/run_word_count.py --input data/transactions_sample.csv --column category

# Agregacja transakcji
python src/run_transactions_agg.py --input data/transactions_sample.csv --top 3

# Statystyki IMDb – gatunki
python src/jobs/imdb_genre_stats.py --input data/imdb.csv --top 20

# Statystyki IMDb – lata urodzenia
python src/jobs/imdb_year_stats.py --input data/imdb.csv --start 1990 --end 2024

# Eksploracja danych
# Podstawowa eksploracja
python src/eda.py --input data/transactions_sample.csv

# Klasteryzacja IMDb
python src/imdb_clustering.py --input data/imdb.csv --k 6

# Wizualizacja wyników
# Transakcje przykładowe
python src/visualize.py --input data/transactions_sample.csv

# Dane IMDb
python src/visualize_imdb.py --input data/imdb.csv
