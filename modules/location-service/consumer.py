import os

from kafka import KafkaConsumer
from utils import save_location

TOPIC_NAME = os.environ["TOPIC_NAME"]
KAFKA_SERVER = os.environ["KAFKA_SERVER"]

# Create the kafka consumer
consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=[KAFKA_SERVER])

while True:
    for message in consumer:
        location_data = message.value.decode('utf-8')
        
        save_location(location_data)
