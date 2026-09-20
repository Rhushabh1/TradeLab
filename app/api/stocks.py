from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.stock import StockResponse
from app.services.stock_service import StockService 


router = APIRouter(prefix = "/stocks",
					tags = ["Stocks"])
service = StockService()


# all the heavy-lifting done by the stockservice
@router.get("/{ticker}", response_model = StockResponse)
def get_stock(ticker: str, db: Session = Depends(get_db)):
	return service.get_stock(db, ticker)