from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.dependencies import get_current_user_id
from app.schemas.portfolio import BuyRequest, SellRequest
from app.services.portfolio_service import PortfolioService 


router = APIRouter(prefix = "/portfolio",
					tags = ["Portfolio"])

service = PortfolioService()


# all the heavy-lifting done by the portfolioservice
@router.post("/buy", response_model = BuyRequest)
def buy(ticker: str, quantity: int, db: Session = Depends(get_db),
		user_id: int = Depends(get_current_user_id)):
	return service.buy(db, user_id, ticker, quantity)


@router.post("/sell", response_model = SellRequest)
def sell(ticker: str, quantity: int, db: Session = Depends(get_db),
		user_id: int = Depends(get_current_user_id)):
	return service.sell(db, user_id, ticker, quantity)


@router.get("/")
def summary(db: Session = Depends(get_db),
			user_id: int = Depends(get_current_user_id)):
	return service.summary(db, user_id)


@router.get("/transactions")
def transactions(db: Session = Depends(get_db),
				user_id: int = Depends(get_current_user_id)):
	return service.transactions(db, user_id)
