from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago
from docker.types import Mount
from script_kafka import kafka_producer_script
from script_kafka import kafka_topic_creation
from airflow.operators.python import (PythonOperator,)
from create_tables import create_tables
from create_lookup_table_script import create_lookup_table
# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
}

# Define the DAG
dag = DAG(
    'purchase_dag',
    default_args=default_args,
    description='A simple DAG to run a job for running an end to end data engineering project. ',
    schedule_interval='@daily',
    start_date=days_ago(1),
    tags=['spark','pyspark','kafka','postgres'],
)

#pythonOperator to create Kafka Topic
task_kafka_topic_creation = PythonOperator(task_id="kafka_topic_creation",python_callable=kafka_topic_creation,dag=dag )


# PythonOperator to send messages to Kafka Producer
task_kafka_producer = PythonOperator(task_id="kafka_producer",python_callable=kafka_producer_script,dag=dag )

#PythonOperator to create Bronze,Silver,Gold tables
task_create_tables = PythonOperator(task_id="table_creation",python_callable=create_tables,dag=dag)
    
    
#PythonOperator to create Loookup_Category table
task_create_lookup_table = PythonOperator(task_id="create_lookup_table_script",python_callable=create_lookup_table,dag=dag)
    
# DockerOperator to run the Bronze Layer job
run_pyspark_job = DockerOperator(
    task_id='run_pyspark_job',
    image='bitnami/spark:latest',
    api_version='auto',
    auto_remove=True,
    command='spark-submit /opt/bitnami/spark/scripts/load_bronze_table.py',
    docker_url='tcp://docker-proxy:2375',  # Ensure this is the correct Docker URL
    network_mode='airflow-kafka',
    environment={'SPARK_LOCAL_HOSTNAME': 'localhost'},
    mounts=[Mount(source='/home/arun/Desktop/dhaarini/DataEngineer/Projects/Project_1/scripts', target='/opt/bitnami/spark/scripts',   type='bind')],
    dag=dag,
)

#  Task dependencies
task_kafka_topic_creation >> task_kafka_producer >> task_create_tables >> task_create_lookup_table