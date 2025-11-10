import os, subprocess, sys, json

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA = os.path.join(ROOT, 'data', 'transactions_sample.csv')
PY = sys.executable or 'python'

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(r.stdout)
    if r.returncode != 0:
        print(r.stderr)
    return r.returncode == 0

if __name__ == '__main__':
    os.makedirs(os.path.join(ROOT,'output'), exist_ok=True)
    status = {
        'test': run([PY, 'tests/test_mapreduce_engine.py']),
        'word_count': run([PY, 'src/run_word_count.py', '--input', DATA, '--column', 'category', '--top', '5']),
        'agg': run([PY, 'src/run_transactions_agg.py', '--input', DATA, '--top', '3']),
        'eda': run([PY, 'src/eda.py', '--input', DATA]),
        'viz': run([PY, 'src/visualize.py', '--input', DATA])
    }
    overall = all(status.values())
    with open(os.path.join(ROOT,'output','quality_gates.json'),'w',encoding='utf-8') as f:
        json.dump({'status':'PASS' if overall else 'FAIL'}, f, ensure_ascii=False)
    print('PASS' if overall else 'FAIL')
