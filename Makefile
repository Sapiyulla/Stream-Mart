spark-run:
	@docker exec -it streammart-spark-master //opt/spark/bin/spark-submit \
		--deploy-mode client \
		//opt/spark/jobs/extract_job.py

spark-run_lvl-warn:
	@make spark-run 2>&1 | grep -E "WARN|ERROR"

start:
	docker compose -f docker-compose.yml up -d
	make spark-run
	@echo "For see info into Spark cluster, open http://localhost:8080"
