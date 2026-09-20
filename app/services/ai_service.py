from datetime import datetime
from uuid import uuid4
from sqlalchemy.orm import Session

from app.core.exceptions import TradeLabException
from app.db.models import AIRequest
from shared.kafka import send_ai_request


REQ_LIMIT = 20
TERMINAL_STATES = ["COMPLETED", "FAILED"]

# used by both API & AI workers via kafka
class AIService:
	# user enters via API
	def submit_question(self, db: Session, user_id: int, question: str):
		question = question.strip()
		request = AIRequest(id = str(uuid4()),
							user_id = user_id,
							question = question,
							status = "QUEUED")
		db.add(request)
		db.commit()
		db.refresh(request)
		# sending request to kafka producer -> consumed by AI worker
		send_ai_request(request_id)
		return request


	# fetch a specific request for user
	def get_user_request(self, db: Session, user_id: int, request_id: str):
		request = (db.query(AIRequest)
					.filter(AIRequest.id == request_id, 
							AIRequest.user_id == user_id)
					.first())
		if request is None:
			raise TradeLabException("AI request not foud", status_code = 404)
		return request


	# list all of user's requests
	def list_user_requests(self, db: Session, user_id: int, limit: REQ_LIMIT):
		return (db.query(AIRequest)
				.filter(AIRequest.user_id == user_id)
				.order_by(AIRequest.created_at.desc())
				.limit(limit)
				.all())


	# to be used by AI worker
	def start_processing(self, db: Session, request_id: str):
		request = (db.query(AIRequest)
					.filter(AIRequest.id == request_id)
					.with_for_update()
					.first())
		if request is None or request.status in TERMINAL_STATES:
			return None
		request.status = "PROCESSING"
		request.updated_at = datetime.now()
		db.commit()
		db.refresh(request)
		return request


	def mark_completed(self, db: Session, request_id: str, answer: str):
		request = (db.query(AIRequest)
					.filter(AIRequest.id == request_id)
					.with_for_update()
					.first())
		if request is None or request.status == "COMPLETED":
			return None
		request.answer = answer
		request.status = "COMPLETED"
		request.updated_at = datetime.now()
		db.commit()


	def mark_failed(self, db: Session, request_id: str):
		request = (db.query(AIRequest)
					.filter(AIRequest.id == request_id)
					.with_for_update()
					.first())
		if request is None or request.status == "COMPLETED":
			return None
		request.status = "FAILED"
		request.updated_at = datetime.now()
		db.commit()