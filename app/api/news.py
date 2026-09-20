from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.dependencies import get_current_user_id
from app.schemas.news import NewsResponse
from app.services.news_service import NewsService 


router = APIRouter(prefix = "/news",
					tags = ["News"])
service = NewsService()


@router.get("/{ticker}", response_model = NewsResponse)
def news(ticker: str, db: Session = Depends(get_db),
		user_id: int = Depends(get_current_user_id)):
	return service.get_news(db, user_id, ticker)