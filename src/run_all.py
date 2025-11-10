"""Skrypt automatyczny uruchamiający: test silnika, word count, agregacje, EDA, wizualizacje.
Użycie:
  python src/run_all.py
"""
import os, json, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA = os.path.join(ROOT, 'data', 'transactions_sample.csv')
PY = sys.executable or 'python'

steps = [
    ("Test silnika", [PY, os.path.join(ROOT, 'tests', 'test_mapreduce_engine.py')]),
    ("Word count", [PY, os.path.join(ROOT, 'src', 'run_word_count.py'), '--input', DATA, '--column', 'category', '--top', '5']),
    ("Agregacje transakcji", [PY, os.path.join(ROOT, 'src', 'run_transactions_agg.py'), '--input', DATA, '--top', '3']),
    ("EDA", [PY, os.path.join(ROOT, 'src', 'eda.py'), '--input', DATA]),
    ("Wizualizacje", [PY, os.path.join(ROOT, 'src', 'visualize.py'), '--input', DATA]),
]

def run_step(name, cmd):
    print(f"\n=== {name} ===")
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(res.stdout)
        if res.stderr.strip():
            print("[stderr]", res.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print("[ERROR]", e)
        print(e.stdout)
        print(e.stderr)
        return False

if __name__ == '__main__':
    all_ok = True
    for name, cmd in steps:
        ok = run_step(name, cmd)
        all_ok = all_ok and ok
    print("\n=== Quality Gates Summary ===")
    print("PASS" if all_ok else "FAIL")
    with open(os.path.join(ROOT, 'output', 'quality_gates.json'), 'w', encoding='utf-8') as f:
        json.dump({"status": "PASS" if all_ok else "FAIL"}, f, indent=2, ensure_ascii=False)
    print("Zapisano output/quality_gates.json")
