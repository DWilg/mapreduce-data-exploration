"""Wizualizacje minimalne."""
import argparse, os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def visualize(path: str):
    df = pd.read_csv(path, parse_dates=['timestamp'])
    os.makedirs('reports', exist_ok=True)
    sns.histplot(df['amount'])
    plt.tight_layout()
    plt.savefig('reports/hist_amount.png')
    plt.close()
    cat_sum = df.groupby('category')['amount'].sum().sort_values(ascending=False)
    sns.barplot(x=cat_sum.values, y=cat_sum.index)
    plt.tight_layout()
    plt.savefig('reports/bar_category_sum.png')
    plt.close()

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True)
    a = p.parse_args()
    visualize(a.input)
