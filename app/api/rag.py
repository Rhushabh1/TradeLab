from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.dependencies import get_current_user_id
from app.services.rag_service import RAGService 
from app.schemas.rag import RAGRequest, RAGResponse


router = APIRouter(prefix = "/rag",
					tags = ["RAG"])
service = RAGService()


@router.post("/retrieve", response_model = RAGResponse)
def retrieve(body: RAGRequest, db: Session = Depends(get_db),
			user_id: int = Depends(get_current_user_id)):
	docs = service.retrieve_context(db, user_id, body.question)
	return {
			"documents": docs
			}