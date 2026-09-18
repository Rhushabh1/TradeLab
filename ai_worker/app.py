from consumer import consumer
from llm import generate


for event in consumer:
	message = event.value
	answer = generate(message["question"])
	print(message["request_id"], answer)