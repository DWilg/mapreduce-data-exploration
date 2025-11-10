import argparse, os
try:
    import kagglehub
    from kagglehub import KaggleDatasetAdapter
except ImportError:
    kagglehub = None

DATASET = "ashirwadsangwan/imdb-dataset"
DEFAULT_FILE = "IMDb Dataset.csv" 

def load_imdb(out_path: str, file_path: str = DEFAULT_FILE):
    if kagglehub is None:
        raise RuntimeError("kagglehub not installed. pip install kagglehub")
    df = kagglehub.load_dataset(KaggleDatasetAdapter.PANDAS, DATASET, file_path)
    os.makedirs(os.path.dirname(out_path) or '.', exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"Saved CSV -> {out_path} rows={len(df)}")

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--out', default='data/imdb.csv')
    p.add_argument('--file', default=DEFAULT_FILE)
    a = p.parse_args()
    load_imdb(a.out, a.file)
