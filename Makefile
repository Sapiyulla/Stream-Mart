spark-run:
	@docker exec -it streammart-spark-master //opt/spark/bin/spark-submit \
		--conf "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension" \
		--conf "spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog" \
		--conf "spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem" \
		--conf "spark.hadoop.fs.s3a.endpoint=http://minio:9000" \
		--conf "spark.hadoop.fs.s3a.access.key=minioadmin" \
		--conf "spark.hadoop.fs.s3a.secret.key=minioadmin" \
		--conf "spark.hadoop.fs.s3a.path.style.access=true" \
		--conf "spark.sql.warehouse.dir=s3a://streammart/" \
		--conf "spark.hadoop.hive.metastore.warehouse.dir=s3a://streammart/" \
		--conf "spark.hadoop.hive.metastore.uris=thrift://hive-metastore:9083" \
		--conf "spark.sql.hive.metastore.version=2.3.9" \
		--conf "spark.sql.hive.metastore.jars=builtin" \
		--conf "spark.sql.catalogImplementation=hive" \
		--conf "spark.hadoop.fs.s3a.aws.credentials.provider=org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider" \
		--deploy-mode client \
		--conf spark.jars.ivy=//tmp/.ivy2 \
		--conf spark.executor.memory=1g \
		--conf spark.executor.cores=1 \
		--conf spark.driver.memory=1g \
		//opt/spark/jobs/extract_job.py

spark-run_lvl-warn:
	@make spark-run 2>&1 | grep -E "WARN|ERROR"

start:
	docker compose -f docker-compose.yml up -d
	make spark-run
	@echo "For see info into Spark cluster, open http://localhost:8080"
