from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName('KafkaStreaming_Extract') \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
    .config("spark.hadoop.fs.s3a.access.key", "minioadmin") \
    .config("spark.hadoop.fs.s3a.secret.key", "minioadmin") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false") \
    .config("spark.jars.packages",
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0,"
            "org.apache.hadoop:hadoop-aws:3.3.4") \
    .master("spark://spark-master:7077") \
    .getOrCreate()
    
df = spark.readStream \
    .format('kafka') \
    .option('kafka.bootstrap.servers', 'kafka:9092') \
    .option('subscribe', 'test_item_liked') \
    .load()


query = df.writeStream \
    .format('parquet') \
    .outputMode('append') \
    .option('path', 's3a://streammart/raw') \
    .option("checkpointLocation", "s3a://meta/checkpoints") \
    .trigger(processingTime="10 seconds") \
    .start()
    
query.awaitTermination()