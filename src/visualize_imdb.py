import argparse, os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme()

def visualize_imdb(path: str):
    df = pd.read_csv(path)
    genre_col = 'genre' if 'genre' in df.columns else 'Genre'
    rating_col = 'rating' if 'rating' in df.columns else 'Rating'
    year_col = 'year' if 'year' in df.columns else 'Year'

    # Genre popularity (count)
    genres_expanded = []
    for raw in df[genre_col].fillna(''):
        for g in [g.strip() for g in str(raw).split(',') if g.strip()]:
            genres_expanded.append(g)
    g_series = pd.Series(genres_expanded)
    top_genres = g_series.value_counts().head(20)
    plt.figure(figsize=(8,5))
    sns.barplot(x=top_genres.values, y=top_genres.index)
    plt.title('Top gatunki (liczność)')
    plt.tight_layout()
    os.makedirs('reports', exist_ok=True)
    plt.savefig('reports/imdb_top_genres.png')
    plt.close()

    # Rating trend over years
    if year_col in df.columns:
        year_stats = df.groupby(year_col)[rating_col].mean().sort_index()
        plt.figure(figsize=(9,4))
        sns.lineplot(x=year_stats.index, y=year_stats.values)
        plt.title('Średnia ocena filmów w czasie')
        plt.tight_layout()
        plt.savefig('reports/imdb_rating_trend.png')
        plt.close()

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True)
    a = p.parse_args()
    visualize_imdb(a.input)
    print('Wygenerowano reports/imdb_top_genres.png oraz imdb_rating_trend.png')
