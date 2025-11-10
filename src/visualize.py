"""Wizualizacje podstawowe rozszerzone.

Generowane wykresy:
1. Histogram kwot transakcji (+ KDE)
2. Suma kwot wg kategorii (bar chart)
3. Kwoty w czasie (line chart)
4. Boxplot rozkładu kwoty per kategoria
5. Scatter user_id vs amount (kolor = kategoria) – przydatny do wglądu w wzorce użytkowników
"""
import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

sns.set_theme(style="whitegrid")

def visualize(path: str):
    df = pd.read_csv(path, parse_dates=['timestamp'])
    os.makedirs('reports', exist_ok=True)

    plt.figure(figsize=(6,4))
    sns.histplot(df['amount'], bins=10, kde=True)
    plt.title('Rozkład kwot transakcji')
    plt.tight_layout()
    plt.savefig('reports/hist_amount.png')
    plt.close()

    plt.figure(figsize=(6,4))
    cat_sum = df.groupby('category')['amount'].sum().sort_values(ascending=False)
    sns.barplot(x=cat_sum.values, y=cat_sum.index)
    plt.title('Suma kwot wg kategorii')
    plt.tight_layout()
    plt.savefig('reports/bar_category_sum.png')
    plt.close()

    df_sorted = df.sort_values('timestamp')
    plt.figure(figsize=(6,4))
    sns.lineplot(x=df_sorted['timestamp'], y=df_sorted['amount'])
    plt.title('Kwoty w czasie')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('reports/line_amount_time.png')
    plt.close()

    plt.figure(figsize=(7,4))
    sns.boxplot(data=df, x='category', y='amount')
    plt.title('Rozkład kwot per kategoria')
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig('reports/box_amount_by_category.png')
    plt.close()

    plt.figure(figsize=(6,4))
    sns.scatterplot(data=df, x='user_id', y='amount', hue='category')
    plt.title('User vs Amount (kolor=kategoria)')
    plt.tight_layout()
    plt.savefig('reports/scatter_user_amount.png')
    plt.close()

    print("Wygenerowano wykresy w folderze reports/ (hist, bar, line, box, scatter)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wizualizacje")
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    visualize(args.input)
