"""Eksploracja danych transakcyjnych.

Rozszerzone kroki:
1. Podgląd, info, statystyki.
2. Tabela braków (missing values) i procentowy udział.
3. Agregacje wg kategorii.
4. Rozkład liczności kategorii.
5. Korelacje numerycznych kolumn (jeśli dostępne) zapisane do CSV.
"""
import argparse
import pandas as pd
import os

def eda(path: str):
    df = pd.read_csv(path)
    print("== Podgląd ==")
    print(df.head())
    print("\n== Info ==")
    print(df.info())
    print("\n== Statystyki kwot ==")
    print(df['amount'].describe())

    by_cat = df.groupby('category')['amount'].agg(['count', 'sum', 'mean']).sort_values('sum', ascending=False)
    print("\n== Agregacje wg kategorii ==")
    print(by_cat)

    print("\n== Missing values ==")
    miss = df.isna().sum().to_frame(name='missing')
    miss['missing_pct'] = (miss['missing'] / len(df) * 100).round(2)
    print(miss)

    print("\n== Liczność kategorii ==")
    print(df['category'].value_counts())

    num_cols = [c for c in df.columns if df[c].dtype != 'object']
    if num_cols:
        corr = df[num_cols].corr()
        print("\n== Macierz korelacji numerycznych ==")
        print(corr)
    else:
        corr = None

    os.makedirs('output', exist_ok=True)
    by_cat.to_csv('output/agg_by_category.csv')
    miss.to_csv('output/missing_summary.csv')
    if corr is not None:
        corr.to_csv('output/correlation_matrix.csv')
    print("Zapisano output/agg_by_category.csv")
    print("Zapisano output/missing_summary.csv")
    if corr is not None:
        print("Zapisano output/correlation_matrix.csv")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EDA transakcji")
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    eda(args.input)
