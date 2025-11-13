"""PySpark word count over a column in a CSV file.
Usage:
  python src/spark_word_count.py --input data/transactions_sample.csv --column category --top 10
"""
from __future__ import annotations
from pyspark.sql import SparkSession


def spark_word_count(path: str, column: str = "category", top: int = 10):
    spark = (SparkSession.builder
             .appName("SparkWordCount")
             .getOrCreate())
    df = spark.read.option("header", True).csv(path)
    if column not in df.columns:
        raise SystemExit(f"Column '{column}' not found. Available: {df.columns}")
    base = df.select(column).na.fill("")
    tokens = (base.rdd
              .flatMap(lambda row: str(row[0]).replace(',', ' ').replace('.', ' ').split())
              .filter(lambda w: w)
              .map(lambda w: (w.lower(), 1))
              .reduceByKey(lambda a, b: a + b))
    results = tokens.takeOrdered(top, key=lambda kv: -kv[1])
    for word, count in results:
        print(f"{word}: {count}")
    spark.stop()


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="PySpark word count (CSV column)")
    p.add_argument("--input", required=True, help="Path to CSV file")
    p.add_argument("--column", default="category", help="Column to tokenize")
    p.add_argument("--top", type=int, default=10, help="Top N words")
    a = p.parse_args()
    spark_word_count(a.input, a.column, a.top)
