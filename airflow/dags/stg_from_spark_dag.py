from airflow.operators.python import PythonOperator
from airflow import DAG

def extract_yesterday():
    pass

with DAG(
    "staging_dag",
    "Get raw data from MinIO and stage to silver",
    schedule_interval="0 2 * * *",
    catchup=False,
    tags=['staging','silver','deltalake','minio']
) as dag:
    extract_task = PythonOperator(
        task_id="extract",
        python_callable=extract_yesterday
    )
    
    extract_yesterday # type: ignore