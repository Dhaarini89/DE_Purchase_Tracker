from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    DateType,
    DecimalType,
    IntegerType,
)
from pyspark.sql.functions import from_json, col
from pyspark.sql import functions as F
import logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s:%(funcName)s:%(levelname)s:%(message)s"
)
POSTGRES_URL = f"jdbc:postgresql://postgres:5432/postgres"
POSTGRES_PROPERTIES = {
    "user": "airflow",
    "password": "airflow",
    "driver": "org.postgresql.Driver",
}

def create_spark_session() -> SparkSession:
    spark = (
        SparkSession.builder.appName("PostgreSQL Connection with PySpark")
        .config(
            "spark.jars.packages",
            "org.postgresql:postgresql:42.5.4,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0",

        )
        .getOrCreate()
    )

    logging.info("Spark session created successfully")
    return spark
def create_initial_dataframe(spark_session):
    """
    Reads the streaming data and creates the initial dataframe accordingly.
    """
    try:
        # Gets the streaming data from topic random_names
        df = (
            spark_session.readStream.format("kafka")
            .option("kafka.bootstrap.servers", "kafka:9092")
            .option("subscribe", "topic_purchase_tracker")
            .option("startingOffsets", "earliest")
            .load()
        )
        logging.info("Initial dataframe created successfully")
    except Exception as e:
        logging.warning(f"Initial dataframe couldn't be created due to exception: {e}")
        raise

    return df

def create_final_dataframe(df):
    # Define the schema as above
    schema = StructType([
    StructField("item_name", StringType(), True),
    StructField("date_of_purchase", DateType(), True),
    StructField("cost", DecimalType(10, 2), True),
    StructField("quantity", IntegerType(), True),
    StructField("purchased_by", StringType(), True),
    StructField("payment_method", StringType(), True)
    ])
    df_out = (
        df.selectExpr("CAST(value AS STRING)")
        .select(from_json(col("value"), schema).alias("data"))
        .select("data.*")
    )
    return df_out

def start_bronze_loading(df_parsed, spark):
    """
    Starts the streaming to table spark_streaming.rappel_conso in postgres
    """
    # Read existing data from PostgreSQL
    existing_data_df = spark.read.jdbc(
        POSTGRES_URL, "bronze_purchase_load", properties=POSTGRES_PROPERTIES
    )

    unique_column = "item_name"

    logging.info("Start streaming ...")
    query = df_parsed.writeStream.foreachBatch(
        lambda batch_df, _: (
            batch_df.join(
                existing_data_df, batch_df[unique_column] == existing_data_df[unique_column], "leftanti"
            )
            .write.jdbc(
                POSTGRES_URL, "bronze_purchase_load", "append", properties=POSTGRES_PROPERTIES
            )
        )
    ).trigger(once=True) \
        .start()

    return query.awaitTermination()

def start_silver_loading(spark):
    # Read bronze data from PostgreSQL
    bronze_data_df = spark.read.jdbc(
        POSTGRES_URL, "bronze_purchase_load", properties=POSTGRES_PROPERTIES
    )

    lookup_category_df = spark.read.jdbc(
         POSTGRES_URL, "lookup_category", properties=POSTGRES_PROPERTIES
    )

    # Perform the join operation on "item_name"
    joined_df = bronze_data_df.join(lookup_category_df, on="item_name", how="inner")

    # Select specific columns from the joined DataFrame
    selected_columns_df = joined_df.select(
    "item_name",
    "date_of_purchase",
    "cost",
    "quantity",
    "purchased_by",
    "payment_method",
    "item_category"
    )
    # Write the resulting DataFrame into another PostgreSQL table
    selected_columns_df.write.jdbc(
    POSTGRES_URL,
    "silver_purchase_load","append" ,properties=POSTGRES_PROPERTIES )

def start_gold_loading(spark):
     # Read bronze data from PostgreSQL
    silver_data_df = spark.read.jdbc(
        POSTGRES_URL, "silver_purchase_load", properties=POSTGRES_PROPERTIES
    )

    # Extract year and month and combine them into a single column
    selected_columns_df = silver_data_df.withColumn("year_month", F.date_format("date_of_purchase", "yyyyMM"))
    # Group by the new year_month column and aggregate the cost and quantity
    gold_df = selected_columns_df.groupBy("year_month").agg(
    F.sum("cost").alias("total_cost"),
    F.sum("quantity").alias("total_quantity")
    )

    # Write the resulting DataFrame into another PostgreSQL table
    gold_df.write.jdbc(
    POSTGRES_URL,
    "gold_purchase_load","append" ,properties=POSTGRES_PROPERTIES )
    

def write_to_postgres():
    spark = create_spark_session()
    df = create_initial_dataframe(spark)
    df_final = create_final_dataframe(df)
    start_bronze_loading(df_final, spark=spark)
    start_silver_loading(spark)
    start_gold_loading(spark)

   


if __name__ == "__main__":
    write_to_postgres()