import json
from kafka import KafkaProducer

from app.config import settings


_producer = None

def _get_producer():
	# standard kafka producer 
	# topics => ai.requests
	global _producer
	if _producer is None:
		_producer = KafkaProducer(bootstrap_servers = settings.KAFKA_BOOTSTRAP_SERVERS,
								value_serializer = lambda value: json.dumps(value).encode("utf-8"),
								acks = "all",
								retries = 3)
	return _producer


def send_ai_request(request_id: str):
	producer = _get_producer()
	producer.send(settings.KAFKA_AI_TOPIC, {"request_id": request_id})