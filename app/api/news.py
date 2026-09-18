from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.news import NewsResponse
from app.services.news_service import NewsService 


router = APIRouter(prefix = "/news",
					tags = ["News"])

service = NewsService()


@router.get("/{ticker}")
def news(ticker: str, db: Session = Depends(get_db)):
	return service.get_news(db, ticker)