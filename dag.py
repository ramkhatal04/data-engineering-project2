
from datetime import datetime

from airflow.decorators import dag
from airflow.providers.apache.spark.operators.spark_submit import (
    SparkSubmitOperator,
)


@dag(
    dag_id="banking_rds_to_s3",
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["banking", "pyspark", "s3"],
)
def banking_pipeline():

    extract_rds_to_s3 = SparkSubmitOperator(
        task_id="extract_rds_to_s3",
        application="/opt/airflow/dags/banking_etl.py",
        conn_id="spark_default",
        name="banking-data-extraction",
        verbose=True,
    )


banking_pipeline()
