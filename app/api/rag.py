from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.dependencies import get_current_user_id
from app.services.rag_service import RAGService 


router = APIRouter(prefix = "/rag",
					tags = ["RAG"])

service = RAGService()


@router.post("/retrieve")
def retrieve(body: dict):
	docs = service.retrieve(body["question"])
	return {
			"documents": docs
			}