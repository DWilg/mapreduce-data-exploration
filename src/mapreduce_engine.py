from __future__ import annotations
import csv, math, time
from multiprocessing import Pool, cpu_count
from typing import Callable, Iterable, List, Tuple, Dict, Any, Union

Record = Any
MapperFn = Callable[[Record], Iterable[Tuple[Any, Any]]]
ReducerFn = Callable[[Any, List[Any]], Any]

def _chunkify(data: List[Record], n: int) -> List[List[Record]]:
    if n <= 1:
        return [data]
    size = math.ceil(len(data) / n)
    return [data[i:i+size] for i in range(0, len(data), size)]

def _run_mapper_chunk(args):
    chunk, mapper, combiner = args
    pairs: List[Tuple[Any, Any]] = []
    for r in chunk:
        for kv in mapper(r):
            pairs.append(kv)
    if combiner is None:
        return pairs
    g: Dict[Any, List[Any]] = {}
    for k, v in pairs:
        g.setdefault(k, []).append(v)
    out: List[Tuple[Any, Any]] = []
    for k, vals in g.items():
        c = combiner(k, vals)
        if isinstance(c, list):
            for x in c:
                out.append((k, x))
        else:
            out.append((k, c))
    return out

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
    t0 = time.time()
    if n_proc == 1:
        mapped: List[Tuple[Any, Any]] = _run_mapper_chunk((chunks[0], mapper, combiner))
    else:
        with Pool(processes=n_proc) as pool:
            mapped_lists = pool.map(_run_mapper_chunk, [(c, mapper, combiner) for c in chunks])
        mapped = [kv for sub in mapped_lists for kv in sub]
    t1 = time.time()
    groups: Dict[Any, List[Any]] = {}
    for k, v in mapped:
        groups.setdefault(k, []).append(v)
    t2 = time.time()
    results: Dict[Any, Any] = {}
    for k, vals in groups.items():
        results[k] = reducer(k, vals)
    t3 = time.time()
    if verbose:
        print(f"map={t1-t0:.4f}s shuffle={t2-t1:.4f}s reduce={t3-t2:.4f}s keys={len(results)}")
    return results

__all__ = ["run_mapreduce"]
