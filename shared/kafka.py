from kafka import KafkaProducer
import json


# standard kafka producer 
# topics => ai.requests
producer = KafkaProducer(bootstrap_servers = "kafka:9092",
						value_serializer = lambda value: json.dumps(value).encode())