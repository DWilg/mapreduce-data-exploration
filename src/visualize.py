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
    num_cols = [c for c in df.select_dtypes(include='number').columns]
    if len(num_cols) > 1:
        corr = df[num_cols].corr()
        plt.figure(figsize=(6,5))
        sns.heatmap(corr, annot=True, fmt='.2f')
        plt.tight_layout()
        plt.savefig('reports/transactions_corr.png')
        plt.close()
    if {'user_id','category','amount'}.issubset(df.columns):
        cat_codes, _ = pd.factorize(df['category'])
        X = pd.DataFrame({'user_id': df['user_id'], 'category_code': cat_codes})
        y = df['amount']
        from sklearn.ensemble import RandomForestRegressor
        model = RandomForestRegressor(n_estimators=120, random_state=42)
        model.fit(X, y)
        fi = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
        plt.figure(figsize=(6,4))
        sns.barplot(x=fi.values, y=fi.index)
        plt.tight_layout()
        plt.savefig('reports/transactions_feature_importance.png')
        plt.close()

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True)
    a = p.parse_args()
    visualize(a.input)
