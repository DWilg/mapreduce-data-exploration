from typing import Iterable, Tuple, Any
from mapreduce_engine import run_mapreduce
import csv

# Expected columns: genre (possibly comma separated), rating, votes

def mapper(row: dict) -> Iterable[Tuple[Any, Any]]:
    genres_field = row.get('genre') or row.get('Genre') or ''
    rating_raw = row.get('rating') or row.get('Rating')
    votes_raw = row.get('votes') or row.get('Votes')
    try:
        rating = float(rating_raw) if rating_raw not in ('', None) else 0.0
    except ValueError:
        rating = 0.0
    try:
        votes = int(votes_raw) if votes_raw not in ('', None) else 0
    except ValueError:
        votes = 0
    for g in [g.strip() for g in genres_field.split(',') if g.strip()]:
        # Emit (genre, (rating, votes, 1))
        yield g, (rating, votes, 1)


def reducer(key: Any, values: list[Tuple[float, int, int]]):
    sum_rating = 0.0
    sum_votes = 0
    count = 0
    for r, v, c in values:
        sum_rating += r
        sum_votes += v
        count += c
    avg_rating = sum_rating / count if count else 0.0
    avg_votes = sum_votes / count if count else 0.0
    return {
        'count': count,
        'avg_rating': round(avg_rating, 3),
        'avg_votes': round(avg_votes, 1)
    }


def genre_stats(path: str):
    return run_mapreduce(path, mapper=mapper, reducer=reducer, processes=None, read_csv=True)

if __name__ == '__main__':
    import argparse, json, os
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True)
    p.add_argument('--top', type=int, default=20)
    a = p.parse_args()
    results = genre_stats(a.input)
    ranked = sorted(results.items(), key=lambda x: x[1]['count'], reverse=True)[:a.top]
    for g, stats in ranked:
        print(f"{g}: count={stats['count']} avg_rating={stats['avg_rating']} avg_votes={stats['avg_votes']}")
    os.makedirs('output', exist_ok=True)
    with open('output/imdb_genre_stats.json','w',encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print('Zapisano output/imdb_genre_stats.json')
