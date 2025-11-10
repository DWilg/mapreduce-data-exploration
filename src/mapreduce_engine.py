"""Lekki silnik MapReduce (lokalna symulacja).

Kontrakt:
- Wejście: iterable rekordów (np. list wierszy CSV lub dict) albo ścieżka pliku (czytane liniowo).
- mapper(record) -> iterable[(key, value)]
- reducer(key, values_list) -> wynik (dowolny obiekt serializowalny)
- (opcjonalnie) combiner(key, values_list) -> pojedyncza wartość lub lista wartości; działa lokalnie na wyjściu mappera zanim trafi do globalnego shuffle.
- Wynik końcowy: dict[key] = reducer_output

Edge cases:
- Pusty zbiór wejściowy -> pusty wynik
- Mapper zwraca 0 par -> klucz nigdy nie trafia do reduce
- Duża liczba kluczy -> grupowanie może zużywać pamięć (tu: wszystko w RAM)
- Combiner może znacząco zmniejszyć liczbę par klucz-wartość w shuffle.

Parametry wydajności (verbose=True) wypisują czasy faz: map, shuffle, reduce.
"""
from __future__ import annotations
import csv
import math
from multiprocessing import Pool, cpu_count
import time
from typing import Callable, Iterable, List, Tuple, Dict, Any, Union

Record = Any
MapperFn = Callable[[Record], Iterable[Tuple[Any, Any]]]
ReducerFn = Callable[[Any, List[Any]], Any]


def _chunkify(data: List[Record], n_chunks: int) -> List[List[Record]]:
    if n_chunks <= 1:
        return [data]
    size = math.ceil(len(data) / n_chunks)
    return [data[i:i+size] for i in range(0, len(data), size)]


def _run_mapper_chunk(args):
    """Uruchamia mapper na pojedynczym kawałku danych.
    Jeśli podany combiner, agreguje lokalnie wartości danego klucza.
    """
    chunk, mapper, combiner = args
    local_pairs: List[Tuple[Any, Any]] = []
    for record in chunk:
        for kv in mapper(record):
            local_pairs.append(kv)

    if combiner is None:
        return local_pairs

    groups: Dict[Any, List[Any]] = {}
    for k, v in local_pairs:
        groups.setdefault(k, []).append(v)
    combined_out: List[Tuple[Any, Any]] = []
    for k, values in groups.items():
        combined_value = combiner(k, values)
        if isinstance(combined_value, list):
            for cv in combined_value:
                combined_out.append((k, cv))
        else:
            combined_out.append((k, combined_value))
    return combined_out


def run_mapreduce(
    input_source: Union[str, Iterable[Record]],
    mapper: MapperFn,
    reducer: ReducerFn,
    processes: int | None = None,
    read_csv: bool = False,
    csv_has_header: bool = True,
    combiner: Callable[[Any, List[Any]], Any | List[Any]] | None = None,
    verbose: bool = False,
) -> Dict[Any, Any]:
    """Uruchom MapReduce.

    input_source: ścieżka pliku lub iterable rekordów.
    read_csv: jeśli True i input_source to ścieżka, parsuje CSV do listy dict lub list.
    combiner: opcjonalna funkcja lokalnej agregacji wyników mappera (działa per-chunk) – redukuje liczbę par.
    verbose: jeśli True wypisuje czasy faz.
    """
    if processes is None:
        processes = max(1, cpu_count() - 1)

    if isinstance(input_source, str):
        records: List[Record] = []
        if read_csv:
            with open(input_source, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f) if csv_has_header else csv.reader(f)
                for row in reader:
                    records.append(row)
        else:
            with open(input_source, encoding='utf-8') as f:
                for line in f:
                    records.append(line.rstrip('\n'))
    else:
        records = list(input_source)

    if not records:
        return {}

    n_proc = min(processes, len(records))
    chunks = _chunkify(records, n_proc)

    t_start_map = time.time()
    if n_proc == 1:
        mapped: List[Tuple[Any, Any]] = _run_mapper_chunk((chunks[0], mapper, combiner))
    else:
        with Pool(processes=n_proc) as pool:
            mapped_lists = pool.map(_run_mapper_chunk, [(c, mapper, combiner) for c in chunks])
        mapped = [kv for sub in mapped_lists for kv in sub]
    t_end_map = time.time()

    t_start_shuffle = time.time()
    groups: Dict[Any, List[Any]] = {}
    for k, v in mapped:
        groups.setdefault(k, []).append(v)
    t_end_shuffle = time.time()

    t_start_reduce = time.time()
    results: Dict[Any, Any] = {}
    for k, values in groups.items():
        results[k] = reducer(k, values)
    t_end_reduce = time.time()

    if verbose:
        print(f"[MapReduce] map: {t_end_map - t_start_map:.4f}s | shuffle: {t_end_shuffle - t_start_shuffle:.4f}s | reduce: {t_end_reduce - t_start_reduce:.4f}s | keys={len(results)}")
    return results

__all__ = ["run_mapreduce"]
