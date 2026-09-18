from uuid import uuid4
from fastapi import APIRouter

from shared.kafka import producer


router = APIRouter(prefix = "/ai",
					tags = ["AI"])


@router.post("/chat")
def chat(body: dict):
	request_id = str(uuid4())
	producer.send("ai.requests",
					{
						"request_id": request_id,
						"question": body["question"]
					})
	return {
			"request_id": request_id,
			"status": "QUEUED"
			}