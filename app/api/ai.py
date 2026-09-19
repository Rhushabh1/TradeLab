from uuid import uuid4
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.dependencies import get_current_user_id
from shared.kafka import producer


router = APIRouter(prefix = "/ai",
					tags = ["AI"])


@router.post("/chat")
def chat(body: dict, db: Session = Depends(get_db)):
	request_id = str(uuid4())
	# save the request before publishing to kafka
	request = AIRequest(id = request_id,
						question = body["question"],
						status = "QUEUED")
	db.add(request)
	db.commit()
	producer.send("ai.requests",
					{
						"request_id": request_id,
						"question": body["question"]
					})
	return {
			"request_id": request_id,
			"status": "QUEUED"
			}


@router.get("/{request_id}")
def status(request_id: str, db: Session = Depends(get_db)):
	request = (db.query(AIRequest)
				.filter(AIRequest.id == request_id)
				.first())
	return {
			"status": request.status,
			"answer": request.answer
			}