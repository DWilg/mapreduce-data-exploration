from typing import Iterable, Tuple, Any
from mapreduce_engine import run_mapreduce


def mapper(row: dict) -> Iterable[Tuple[Any, Any]]:
    year_raw = row.get('year') or row.get('Year') or ''
    rating_raw = row.get('rating') or row.get('Rating')
    try:
        year = int(year_raw)
    except ValueError:
        return []
    try:
        rating = float(rating_raw) if rating_raw not in ('', None) else 0.0
    except ValueError:
        rating = 0.0
    yield year, (rating, 1)


def reducer(key: Any, values: list[Tuple[float, int]]):
    sum_rating = 0.0
    count = 0
    for r, c in values:
        sum_rating += r
        count += c
    avg_rating = sum_rating / count if count else 0.0
    return {'count': count, 'avg_rating': round(avg_rating, 3)}


def year_stats(path: str):
    return run_mapreduce(path, mapper=mapper, reducer=reducer, processes=None, read_csv=True)

if __name__ == '__main__':
    import argparse, json, os
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True)
    p.add_argument('--start', type=int, default=None)
    p.add_argument('--end', type=int, default=None)
    a = p.parse_args()
    results = year_stats(a.input)
    filtered = {y: stats for y, stats in results.items() if (a.start is None or y >= a.start) and (a.end is None or y <= a.end)}
    ranked = sorted(filtered.items(), key=lambda x: x[0])
    for y, stats in ranked[:50]:
        print(f"{y}: count={stats['count']} avg_rating={stats['avg_rating']}")
    os.makedirs('output', exist_ok=True)
    with open('output/imdb_year_stats.json','w',encoding='utf-8') as f:
        json.dump(filtered, f, ensure_ascii=False, indent=2)
    print('Zapisano output/imdb_year_stats.json')
