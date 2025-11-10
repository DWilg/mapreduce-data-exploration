from jobs.word_count import word_count

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Runner: word count")
    parser.add_argument("--input", required=True)
    parser.add_argument("--column", default="category")
    parser.add_argument("--top", type=int, default=10)
    args = parser.parse_args()
    results = word_count(args.input, args.column)
    sorted_items = sorted(results.items(), key=lambda x: x[1], reverse=True)[:args.top]
    for word, cnt in sorted_items:
        print(f"{word}: {cnt}")
