from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import to_date, col, current_date, from_json, lit
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
    .enableHiveSupport() \
    .master("spark://spark-master:7077") \
    .getOrCreate()

spark.sparkContext.setLogLevel('WARN')

# Проверка подключения к Hive
try:
    spark.sql("SHOW DATABASES").show()
    print("✅ Подключение к Hive Metastore успешно!")
except Exception as e:
    print(f"❌ Ошибка подключения к Hive: {e}")
    print("Проверьте, что Hive Metastore запущен и доступен")

# Создаем базу данных
spark.sql("USE raw")

def write_to_MinIO(batch_df: DataFrame, batch_id: int):
    
    if batch_df.count() == 0:
        return
    
    if 'timestamp' in batch_df.columns:
        batch_df = batch_df.withColumn('date', to_date(col('timestamp')))
    else:
        batch_df = batch_df.withColumn('date', current_date())
    
    if 'topic' not in batch_df.columns:
        batch_df = batch_df.withColumn('topic', lit('unknown'))
    
    batch_df.write \
        .mode('append') \
        .format('delta') \
        .partitionBy('topic', 'date') \
        .option('compression', 'snappy') \
        .option('maxRecordsPerFile', 1000) \
        .saveAsTable('raw.events')
    
    print(f"Batch {batch_id} written: {batch_df.count()} records")

# Чтение из Kafka
df = spark.readStream \
    .format('kafka') \
    .option('kafka.bootstrap.servers', 'kafka:9092') \
    .option("subscribePattern", "item_.*") \
    .option("startingOffsets", "latest") \
    .load() \
    .select(from_json(col("value").cast("string"), schema).alias("data"), col("topic")) \
    .select("data.*", "topic")

# Запись в Hive через Streaming
query = df.writeStream \
    .outputMode('append') \
    .foreachBatch(write_to_MinIO) \
    .option('checkpointLocation', 's3a://meta/checkpoints/') \
    .trigger(processingTime='10 seconds') \
    .start()

print("✅ Streaming started...")
query.awaitTermination()