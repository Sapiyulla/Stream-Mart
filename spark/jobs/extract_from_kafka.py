from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import to_date, col, current_date, from_json
from pyspark.sql.types import StructType, StructField, StringType, FloatType, IntegerType

schema = StructType([
    StructField("event_id", StringType()),
    StructField("event_type", StringType()),
    StructField("timestamp", StringType()),
    StructField("payload", StructType([
        StructField("user_id", IntegerType()),
        StructField("item_id", IntegerType()),
        StructField("category", StringType()),
        StructField("price", FloatType()),
        StructField("quantity", IntegerType()),
        StructField("rating", IntegerType()),
        StructField("reason", StringType()),
    ])),
])

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
    
    
# set only WARN and ERROR logs (ONLY FOR DEVELOP!)
spark.sparkContext.setLogLevel('WARN')
    

def write_to_MinIO(batch_df: DataFrame, batch_id: int):
    if batch_df.count() == 0:
        return
        
    batch_df.write \
        .mode('append') \
        .format('parquet') \
        .partitionBy('topic', 'date') \
        .option('compression', 'snappy') \
        .option('maxRecordsPerFile', 1000) \
        .save('s3a://streammart/raw')

    
# connect to Kafka topic
df = spark.readStream \
    .format('kafka') \
    .option('kafka.bootstrap.servers', 'kafka:9092') \
    .option("subscribePattern", "item_.*") \
    .load() \
    .select(from_json(col("value").cast("string"), schema).alias("data"), col("topic")) \
    .select("data.*", "topic")

# processing DataFrame
if 'timestamp' in df.columns:
    df = df.withColumn('date', to_date(col('timestamp')))
else:
    df = df.withColumn('date', current_date())
    
# save to MinIO with use writeStream from Spark
query = df.writeStream \
    .outputMode('append') \
    .foreachBatch(write_to_MinIO) \
    .option('checkpointLocation', 's3a://meta/checkpoints') \
    .trigger(processingTime='10 seconds') \
    .start()

query.awaitTermination()