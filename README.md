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
```

## Spark (opcjonalnie)
Dodaliśmy równoległe przykłady w PySpark, aby pokazać skalowalną wersję przetwarzania.

### Instalacja dodatkowa
```bash
pip install pyspark
# lub
pip install -r requirements-spark.txt
```

### Word Count w Spark
```bash
python src/spark_word_count.py --input data/transactions_sample.csv --column category --top 10
```

### Agregacja transakcji w Spark
```bash
python src/spark_transactions_agg.py --input data/transactions_sample.csv --top 5
```

### (Opcjonalnie) ETL do Parquet
```bash
python src/spark_clean_transactions.py --input data/transactions_sample.csv --out data/processed/transactions.parquet
```

### Porównanie lokalne vs Spark
| Aspekt | Lokalny MapReduce | Spark |
|--------|-------------------|-------|
| Skalowalność | CPU lokalne (multiprocessing) | Klaster / executors |
| API | Własne map/reduce | RDD + DataFrame + SQL + MLlib |
| Format danych | CSV | Parquet, CSV, inne |
| ML | scikit-learn w notebooku | MLlib / pipeline |
| Czas startu | Bardzo szybki | Wolniejszy (inicjalizacja JVM) |

Notebook demonstracyjny: `notebooks/BigData.ipynb` (pipeline EDA + model). Planowany notebook PySpark: `notebooks/PySparkDemo.ipynb`.

## Raporty i artefakty
Po uruchomieniu skryptów w folderach `output/` i `reports/` pojawią się:
- `output/transactions_agg.json` – wyniki agregacji kategorii
- `output/imdb_genre_stats.json`, `output/imdb_year_stats.json` – statystyki IMDb
- `reports/hist_amount.png`, `reports/bar_category_sum.png`, `reports/transactions_corr.png` – wizualizacje transakcji
- `reports/imdb_top_genres.png`, `reports/imdb_rating_trend.png` – wizualizacje IMDb

## Jakość / automatyczny pipeline
Uruchomienie całości:
```bash
python src/run_all.py
```
Tworzy plik `output/quality_gates.json` z informacją PASS/FAIL.

## Następne kroki (możliwe rozszerzenia)
- Benchmark lokalny vs Spark dla większego pliku
- Dodanie klastrowania w Spark MLlib
- Konwersja do formatu Parquet z partycjonowaniem po roku
- Dodanie TF-IDF dla opisu filmów (Overview) w MapReduce / Spark

