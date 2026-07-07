FROM alpine:3.20 AS dependencies

ARG HADOOP_VERSION=3.3.4
ARG DELTA_VERSION=2.4.0
ARG AWS_BUNDLE_VERSION=1.12.262
ARG SPARK_VERSION=3.4.0
ARG KAFKA_VERSION=3.4.0
ARG KAFKA_CLIENTS_VERSION=3.3.2
ARG COMMONS_POOL_VERSION=2.11.1

RUN apk add --no-cache curl

WORKDIR /downloads

# Hadoop AWS
RUN curl -fsSL \
    https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/${HADOOP_VERSION}/hadoop-aws-${HADOOP_VERSION}.jar \
    -o hadoop-aws-${HADOOP_VERSION}.jar

# AWS SDK Bundle
RUN curl -fsSL \
    https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/${AWS_BUNDLE_VERSION}/aws-java-sdk-bundle-${AWS_BUNDLE_VERSION}.jar \
    -o aws-java-sdk-bundle-${AWS_BUNDLE_VERSION}.jar

# Delta Lake
RUN curl -fsSL \
    https://repo1.maven.org/maven2/io/delta/delta-core_2.12/${DELTA_VERSION}/delta-core_2.12-${DELTA_VERSION}.jar \
    -o delta-core-${DELTA_VERSION}.jar

# Delta Storage
RUN curl -fsSL \
    https://repo1.maven.org/maven2/io/delta/delta-storage/${DELTA_VERSION}/delta-storage-${DELTA_VERSION}.jar  \
    -o delta-storage-${DELTA_VERSION}.jar

# Spark Kafka connector
RUN curl -fsSL \
    https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/${KAFKA_VERSION}/spark-sql-kafka-0-10_2.12-${KAFKA_VERSION}.jar \
    -o spark-sql-kafka-0-10_2.12-${KAFKA_VERSION}.jar

RUN curl -fsSL \
    https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.12/${KAFKA_VERSION}/spark-token-provider-kafka-0-10_2.12-${KAFKA_VERSION}.jar \
    -o spark-token-provider-kafka-0-10_2.12-${KAFKA_VERSION}.jar

RUN curl -fsSL \
    https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/${KAFKA_CLIENTS_VERSION}/kafka-clients-${KAFKA_CLIENTS_VERSION}.jar \
    -o kafka-clients-${KAFKA_CLIENTS_VERSION}.jar

RUN curl -fsSL \
    https://repo1.maven.org/maven2/org/apache/commons/commons-pool2/${COMMONS_POOL_VERSION}/commons-pool2-${COMMONS_POOL_VERSION}.jar \
    -o commons-pool2-${COMMONS_POOL_VERSION}.jar

# stage 2
FROM apache/spark-py:v3.4.0

USER root

COPY --from=dependencies \
    /downloads/*.jar \
    /opt/spark/jars/