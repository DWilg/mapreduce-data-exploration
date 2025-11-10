# Projekt Big Data – MapReduce, Eksploracja Danych i Wizualizacja

## Cel
Projekt demonstruje model przetwarzania danych MapReduce (symulacja lokalna w Pythonie), podstawową eksplorację danych (EDA) oraz wizualizację wyników.

## Zawartość
- `src/mapreduce_engine.py` – lekki silnik MapReduce (map, shuffle, reduce, równoległość przez multiprocessing)
- `src/jobs/word_count.py` – przykład zliczania słów
- `src/jobs/transactions_agg.py` – agregacje transakcji: suma, średnia, top kategorie
- `src/run_word_count.py` / `src/run_transactions_agg.py` – skrypty uruchamiające przykładowe zadania
- `data/transactions_sample.csv` – przykładowy zbiór transakcji
- `src/eda.py` – eksploracja danych z użyciem pandas
- `src/visualize.py` – generowanie wykresów do folderu `reports/`
- `tests/test_mapreduce_engine.py` – testy podstawowe silnika
 - `src/run_all.py` – automatyczny pipeline (test, joby, EDA, wizualizacje)

## Wymagania
Patrz `requirements.txt`. Instalacja (PowerShell):
```pwsh
pip install -r requirements.txt
```

## Uruchomienie przykładowego zadania Word Count
```pwsh
python src/run_word_count.py --input data/transactions_sample.csv --column category
```
(Powyżej używamy kolumny `category` tylko jako źródła krótkich "słów" – można przygotować osobny plik tekstowy.)

## Uruchomienie agregacji transakcji
```pwsh
python src/run_transactions_agg.py --input data/transactions_sample.csv --top 3
```

## Eksploracja danych
```pwsh
python src/eda.py --input data/transactions_sample.csv
```
Wyniki statystyk pojawią się w konsoli, wybrane tabele zapisane w `output/`.

## Wizualizacja
```pwsh
python src/visualize.py --input data/transactions_sample.csv
```
Wykresy PNG zapisane w `reports/`.

## Model MapReduce (skrót)
1. Podział wejścia na porcje (split)
2. Równoległe wykonanie funkcji `mapper(record)` → [(key, value), ...]
3. Faza shuffle: grupowanie wartości według klucza
4. Faza reduce: `reducer(key, list_of_values)` → wynik

### Combiner (opcjonalny)
Można przekazać do `run_mapreduce` funkcję `combiner(key, values_list)` która lokalnie agreguje wyniki mappera w obrębie chunku przed globalnym shuffle – redukuje ilość przesyłanych par.

### Profilowanie
Parametr `verbose=True` wypisuje czasy faz: map, shuffle, reduce.

## Rozszerzenia / pomysły
- Dodanie notebooka interaktywnego (`notebooks/`)
- Streaming (przetwarzanie porcjami z pliku dużego)
- Persistencja wyników w bazie NoSQL
 - Dodanie kolejnych wizualizacji (heatmapa korelacji, wykres pudełkowy – już zaimplementowany, scatter)
 - Integracja z klastrem Hadoop / Spark (mapowanie API na prawdziwe środowisko rozproszone)

## Licencja
Kod edukacyjny — użycie dowolne w ramach zajęć.
