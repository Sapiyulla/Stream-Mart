FROM alpine:3.20 AS dependencies

ARG HADOOP_VERSION=3.1.0
ARG AWS_BUNDLE_VERSION=1.12.262

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

FROM apache/hive:3.1.3

USER root

COPY --from=dependencies \
    /downloads/*.jar \
    /opt/hive/lib/