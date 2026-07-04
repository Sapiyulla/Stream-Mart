spark-run:
	docker exec -it streammart-spark-master /opt/spark/bin/spark-submit \
                --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0 \
                --deploy-mode client \
                --conf spark.jars.ivy=/tmp/.ivy2 \
                --conf spark.executor.memory=1g \
                --conf spark.executor.cores=1 \
                --conf spark.driver.memory=1g \
                /opt/spark/jobs/extract_from_kafka.py

start:
	docker compose -f docker-compose.yml up -d
	make spark-run
	# For see info into Spark cluster, open http://localhost:8080

