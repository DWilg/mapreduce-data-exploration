from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("Test").getOrCreate()
print("Spark version:", spark.version)
spark.stop()