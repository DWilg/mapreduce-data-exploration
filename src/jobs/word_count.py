from typing import Iterable, Tuple, Any
from mapreduce_engine import run_mapreduce

# Mapper: przyjmuje wiersz (dict z CSV) i emituje (słowo, 1) z kolumny wybranej.

def make_mapper(column: str):
    def mapper(row: dict) -> Iterable[Tuple[Any, Any]]:
        value = str(row.get(column, ""))
        # Rozbij na pseudo-słowa wg znaków nie-alfanumerycznych
        for token in [t for t in value.replace(',', ' ').replace('.', ' ').split() if t]:
            yield token.lower(), 1
    return mapper


def reducer(key: Any, values: list[int]) -> int:
    return sum(values)


def word_count(path: str, column: str = "category"):
    mapper = make_mapper(column)
    return run_mapreduce(path, mapper=mapper, reducer=reducer, processes=None, read_csv=True)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Word count MapReduce (kolumna z pliku CSV)")
    parser.add_argument("--input", required=True)
    parser.add_argument("--column", default="category")
    parser.add_argument("--top", type=int, default=10)
    args = parser.parse_args()
    results = word_count(args.input, args.column)
    sorted_items = sorted(results.items(), key=lambda x: x[1], reverse=True)[:args.top]
    for word, cnt in sorted_items:
        print(f"{word}: {cnt}")
