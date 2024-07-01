FROM apache/airflow:2.9.1

RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" unidecode==1.3.7
# Install git
USER root
RUN apt-get update && apt-get install -y git && apt-get clean



# Switch back to the airflow user
USER airflow
RUN pip install git+https://github.com/dpkp/kafka-python.git

#for Pyspark
RUN pip install pyspark
