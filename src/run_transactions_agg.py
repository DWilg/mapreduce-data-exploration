from jobs.transactions_agg import aggregate_transactions

if __name__ == "__main__":
    import argparse, json, os
    parser = argparse.ArgumentParser(description="Runner: agregacje transakcji")
    parser.add_argument("--input", required=True)
    parser.add_argument("--top", type=int, default=5)
    args = parser.parse_args()
    results = aggregate_transactions(args.input)
    ranked = sorted(results.items(), key=lambda x: x[1]["total"], reverse=True)[:args.top]
    for cat, stats in ranked:
        print(f"{cat}: total={stats['total']:.2f} avg={stats['avg']:.2f} count={stats['count']}")
    out_path = os.path.join("output", "transactions_agg.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Zapisano pełne wyniki do {out_path}")
