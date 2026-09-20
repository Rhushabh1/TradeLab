import json
from kafka import KafkaConsumer

from app.config import settings


# standard kafka consumer
consumer = KafkaConsumer(settings.KAFKA_AI_TOPIC,
						bootstrap_servers = settings.KAFKA_BOOTSTRAP_SERVERS,
						group_id = settings.KAFKA_AI_GROUP_ID,
						enable_auto_commit = False,
						value_deserializer = lambda value: json.loads(value.decode("utf-8")))