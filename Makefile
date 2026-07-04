spark-run:
	@docker exec -it streammart-spark-master /opt/spark/bin/spark-submit \
                --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0,org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262 \
                --deploy-mode client \
                --conf spark.jars.ivy=/tmp/.ivy2 \
                --conf spark.executor.memory=1g \
                --conf spark.executor.cores=1 \
                --conf spark.driver.memory=1g \
                /opt/spark/jobs/extract_from_kafka.py

start:
	docker compose -f docker-compose.yml up -d
	make spark-run
	@echo "For see info into Spark cluster, open http://localhost:8080"

status:
	@echo "=== Containers ==="
	@docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "(NAMES|streammart)"
	@echo ""
	@echo "=== Spark Master ==="
	@docker exec streammart-spark-master //opt/spark/bin/spark-submit --version 2>&1 | head -2 | tail -1 || echo "Spark unavialable"
	@echo ""
	@echo "=== Spark Workers ==="
	@docker exec streammart-spark-master wget -qO- http://localhost:8080 2>/dev/null | grep -o "Alive Workers: [0-9]*" | head -1 || echo "No status"
	@echo ""
	@echo "=== MinIO ==="
	@docker exec streammart-minio mc --version 2>&1 | head -1 || echo "MinIO unavialable (please, check into container)"
	@docker exec streammart-minio mc ls local/ 2>/dev/null | grep -q . && echo "Buckets unavialable" || echo "Buckets not found"
	@echo ""
	@echo "=== Kafka ==="
	@docker exec streammart-kafka //opt/kafka/bin/kafka-topics.sh --bootstrap-server kafka:9092 --list 2>/dev/null || echo "Kafka unavialable"