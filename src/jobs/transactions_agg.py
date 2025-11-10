from typing import Iterable, Tuple, Any
from mapreduce_engine import run_mapreduce


def mapper(row: dict) -> Iterable[Tuple[Any, Any]]:
    try:
        amount = float(row.get("amount", 0))
    except (TypeError, ValueError):
        amount = 0.0
    category = row.get("category", "UNKNOWN")
    yield category, amount


def reducer(key: Any, values: list[float]):
    total = sum(values)
    count = len(values)
    avg = total / count if count else 0.0
    return {"total": total, "count": count, "avg": avg}


def aggregate_transactions(path: str):
    return run_mapreduce(path, mapper=mapper, reducer=reducer, processes=None, read_csv=True)

if __name__ == "__main__":
    import argparse, json
    parser = argparse.ArgumentParser(description="Agregacje transakcji wg kategorii")
    parser.add_argument("--input", required=True)
    parser.add_argument("--top", type=int, default=5)
    args = parser.parse_args()
    results = aggregate_transactions(args.input)
    ranked = sorted(results.items(), key=lambda x: x[1]["total"], reverse=True)[:args.top]
    for cat, stats in ranked:
        print(f"{cat}: total={stats['total']:.2f} avg={stats['avg']:.2f} count={stats['count']}")
    import os
    out_path = os.path.join("output", "transactions_agg.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Zapisano pełne wyniki do {out_path}")
