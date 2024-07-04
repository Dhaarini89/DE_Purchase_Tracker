Purchase Tracker: An End-to-End Data Engineering Project

In this project, I have focused on a simple yet practical concept: tracking daily purchases. The objective is to gain fundamental knowledge and hands-on experience with key technologies in the data engineering stack. The technologies include PostgreSQL, Docker, Kafka, Airflow, Spark, and PySpark. This project will encompass the complete data engineering lifecycle, from data ingestion to processing and storage, following the medallion architecture.

![High_Level_Flow](/DE_Draft.png)

Key Technologies:
PostgreSQL: For structured data storage and querying.
Docker: To create isolated environments for the different components of the project.
Kafka: For real-time data ingestion and streaming.
Airflow: To orchestrate and schedule the data workflows.
Spark & PySpark: For large-scale data processing and analytics.

Medallion Architecture:
The medallion architecture divides data processing into three distinct layers: Bronze, Silver, and Gold.

Bronze Layer:

Raw data ingestion and storage.
Data is stored as-is, without any transformations.
Raw purchase events from Kafka streams.

Silver Layer:
Cleaned and refined data.
Parsed and validated purchase records with necessary transformations applied.

Gold Layer:
Aggregated and business-level data.
Data is transformed for specific business use cases, analytics, and reporting.
Monthly purchase summaries and analytics.

Project Workflow:
Data Ingestion: Use Kafka to stream purchase data in real-time.
Data Storage: Store the streamed data in PostgreSQL for structured querying and storage.
Data Processing: Use Spark and PySpark for processing and analyzing the data.
Workflow Orchestration: Schedule and manage the data pipelines with Airflow.
Containerization: Utilize Docker to ensure the environment consistency across different stages of the project.

Project Goals:
Ingest real-time purchase data using Kafka.
Store the data efficiently in a PostgreSQL database.
Process the data using Spark and PySpark for insights and analytics.
Orchestrate the data pipeline using Airflow to automate the workflows.
Containerize the components using Docker for seamless deployment and management.

Learning Outcomes:
Develop an understanding of how to set up and manage a PostgreSQL database.
Learn to create and manage Docker containers for different services.
Gain experience in setting up and using Kafka for data streaming.
Master the basics of Spark and PySpark for data processing.
Understand how to use Airflow to schedule and monitor data workflows.

By the end of this project, I have built a comprehensive data engineering pipeline capable of ingesting, storing, processing, and analyzing purchase data, providing a solid foundation in the key technologies used in the industry.
