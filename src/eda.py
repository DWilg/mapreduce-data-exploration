"""EDA minimalna."""
import argparse
import pandas as pd
import os

def eda(path: str):
    df = pd.read_csv(path)
    print(df.head())
    print(df['amount'].describe())
    by_cat = df.groupby('category')['amount'].agg(['count','sum','mean']).sort_values('sum', ascending=False)
    print(by_cat)
    os.makedirs('output', exist_ok=True)
    by_cat.to_csv('output/agg_by_category.csv')

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True)
    a = p.parse_args()
    eda(a.input)
