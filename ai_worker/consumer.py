from kafka import KafkaConsumer
import json


# standard kafka consumer
consumer = KafkaConsumer("ai.requests",
						bootstrap_servers = "kafka:9092",
						value_deserializer = lambda value: json.loads(value.decode()))