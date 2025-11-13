"""PySpark aggregation of transactions by category.
Usage:
  python src/spark_transactions_agg.py --input data/transactions_sample.csv --top 5
"""
from __future__ import annotations
from pyspark.sql import SparkSession, functions as F


def spark_transactions_agg(path: str, top: int = 5):
    spark = (SparkSession.builder
             .appName("SparkTransactionsAgg")
             .getOrCreate())
    df = (spark.read
                .option("header", True)
                .option("inferSchema", True)
                .csv(path))
    if 'category' not in df.columns or 'amount' not in df.columns:
        raise SystemExit("Wymagane kolumny: category, amount")
    df = df.withColumn('amount', F.col('amount').cast('double')).filter(F.col('amount').isNotNull())
    agg = (df.groupBy('category')
             .agg(F.count('*').alias('count'),
                  F.sum('amount').alias('total'),
                  F.avg('amount').alias('avg'))
             .orderBy(F.col('total').desc()))
    agg.show(top, truncate=False)
    spark.stop()


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(description='PySpark agregacja transakcji wg kategorii')
    p.add_argument('--input', required=True)
    p.add_argument('--top', type=int, default=5)
    a = p.parse_args()
    spark_transactions_agg(a.input, a.top)
