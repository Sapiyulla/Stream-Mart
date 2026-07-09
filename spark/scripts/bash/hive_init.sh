#!/bin/bash
set -e

echo "Hive Metastore initialization started"

until (echo > /dev/tcp/hive-metastore/9083) >/dev/null 2>&1; do
    echo "Waiting for Hive Metastore"
    sleep 2
done;

echo "Hive Metastore is ready"

/opt/spark/bin/spark-sql -f /opt/spark/sql/hive_init.sql

echo -e "Hive Metastore initialized\n"

# Show databases

echo  "Please, wait..."
sleep 2

echo  "Fetch allowed databases..."

/opt/spark/bin/spark-sql -e "SHOW DATABASES"

echo -e "\nScript executed. Hive Metastore ready for use."