import argparse, os
import pandas as pd
from sklearn.cluster import KMeans

def cluster(path: str, k: int):
    df = pd.read_csv(path)
    rating_col = 'rating' if 'rating' in df.columns else 'Rating'
    votes_col = 'votes' if 'votes' in df.columns else 'Votes'
    work = df[[rating_col, votes_col]].dropna()
    X = work.values
    model = KMeans(n_clusters=k, random_state=42, n_init='auto')
    labels = model.fit_predict(X)
    work['cluster'] = labels
    out = work.groupby('cluster').agg(['count','mean']).to_dict()
    os.makedirs('output', exist_ok=True)
    work.to_csv('output/imdb_clusters.csv', index=False)
    return out

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True)
    p.add_argument('--k', type=int, default=5)
    a = p.parse_args()
    summary = cluster(a.input, a.k)
    print(summary)
    print('Zapisano output/imdb_clusters.csv')
