import json
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic


#Function to create Kafka Topic
def kafka_topic_creation():
  broker = 'kafka:9092'  # Replace with your Kafka broker
  topic_name = 'topic_purchase_tracker'
  num_partitions = 1
  replication_factor = 1
  create_kafka_topic(broker, topic_name, num_partitions, replication_factor)
  
#create topic  
def create_kafka_topic(broker, topic_name, num_partitions=1, replication_factor=1):
     # Create an Admin client
    admin_client = KafkaAdminClient(
        bootstrap_servers=broker,
        client_id='test_admin'
    )

    # Define the new topic
    topic = NewTopic(
        name=topic_name,
        num_partitions=num_partitions,
        replication_factor=replication_factor
    )

    # Attempt to create the topic
    try:
        admin_client.create_topics(new_topics=[topic], validate_only=False)
        print(f"Topic {topic_name} created successfully")
    except Exception as e:
        print(f"Failed to create topic {topic_name}: {e}")
    finally:
        admin_client.close()
  

    
# Function to read JSON file
def read_json_file(file_path):
     # Kafka broker address
    kafka_broker = 'kafka:9092'  # Replace with your Kafka broker address
    
    # Create Kafka producer
    producer = create_kafka_producer(kafka_broker)
   
   
#loading json records one by one
    with open(file_path, 'r') as file:
     for line in file:
        try:
            data = json.loads(line)
            print(data)
            send_to_kafka(producer, data)

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")


# Initialize Kafka Producer
def create_kafka_producer(bootstrap_servers):
    return KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

# Send JSON data to Kafka topic
def send_to_kafka(producer, data):
    producer.send('topic_purchase_tracker', value=data)
    producer.flush()

def kafka_producer_script():
    # File path to the JSON file
    json_file_path = '/opt/airflow/src/purchases.json'
    dataresult=read_json_file(json_file_path)
   

if __name__ == "__main__":
    kafka_producer_script()    
    kafka_topic_creation()

    
    
