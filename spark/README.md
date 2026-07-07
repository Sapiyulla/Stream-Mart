# Spark

> В контексте данного пайплайна Spark используется как вычислительный и стримминговый сервис.

## Info

> Поднято только 2 ноды: **Master** и **Worker**.  
> Тип обработки данных: `stream`.

> Если обобщенно, то он читает из Kafka и пишет в MinIO.

> Для сохранения в MinIO используется `Delta` формат таблиц вместо `Parquet` формата данных.
> Имеет партицирование по **Топикам** и **Датам**.

## Connectors

Service | Connector Plugin (Full) | Version
-|-|-
Apache Kafka | `org.apache.spark:spark-sql-kafka-0-10_2.12` | `3.4.0`
MinIO S3 | `org.apache.hadoop:hadoop-aws` | `3.3.4`