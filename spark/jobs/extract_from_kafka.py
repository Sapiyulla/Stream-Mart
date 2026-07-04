from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName('KafkaStreaming_Extract') \
    .config("spark.jars.packages",
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0") \
    .master("spark://spark-master:7077") \
    .getOrCreate()
    
df = spark.readStream \
    .format('kafka') \
    .option('kafka.bootstrap.servers', 'kafka:9092') \
    .option('subscribe', 'test_item_liked') \
    .load()
    
sq = (df.writeStream.format('console')
    .outputMode("append").start())

sq.awaitTermination()