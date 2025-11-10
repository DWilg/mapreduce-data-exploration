import sys, os
sys.path.append(os.path.abspath('src'))
from mapreduce_engine import run_mapreduce

def mapper(line: str):
    for token in line.split():
        yield token.lower(), 1

def reducer(key, values):
    return sum(values)

def test_word_count_simple():
    data = ["ala ma kota", "kot ma ale"]
    results = run_mapreduce(data, mapper=mapper, reducer=reducer, processes=1)
    assert results['ma'] == 2
    assert results['kot'] == 1 or results['kota'] == 1  # zależnie od tokenizacji

if __name__ == '__main__':
    test_word_count_simple()
    print('Test przeszedł poprawnie.')
