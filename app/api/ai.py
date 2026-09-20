from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.dependencies import get_current_user_id
from app.schemas.ai import AIQuestion, AIRequest, AIResponse
from app.services.ai_service import AIService


router = APIRouter(prefix = "/ai",
					tags = ["AI"])
service = AIService()


@router.post("/chat", response_model = AIRequest)
def submit_question(body: AIQuestion, db: Session = Depends(get_db),
					user_id: int = Depends(get_current_user_id)):
	request = service.submit_question(db, user_id, body.question)
	return {
			"request_id": request.id,
			"status": request.status,
			"created_at": request.created_at
			}


@router.get("/", response_model = list[AIResponse])
def list_requests(limit: int, db: Session = Depends(get_db),
				user_id: int = Depends(get_current_user_id)):
	return service.list_user_requests(db, user_id, limit)


@router.get("/{request_id}", response_model = AIResponse)
def get_request_status(request_id: str, db: Session = Depends(get_db),
						user_id: int = Depends(get_current_user_id)):
	return service.get_user_request(db, user_id, request_id)