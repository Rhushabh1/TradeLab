from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user_id 
from app.db.database import get_db
from app.schemas.watchlist import WatchlistCreate, WatchlistResponse
from app.services.watchlist_service import WatchlistService


router = APIRouter(prefix = "/watchlist",
					tags = ["Watchlist"])
service = WatchlistService()


@router.post("/", response_model = WatchlistResponse)
def add_ticker(body: WatchlistCreate, db: Session = Depends(get_db),
				user_id: int = Depends(get_current_user_id)):
	return service.add_ticker(db, user_id, body.ticker)


@router.get("/", response_model = list[WatchlistResponse])
def list_watchlist(db: Session = Depends(get_db),
					user_id: int = Depends(get_current_user_id)):
	return service.list_watchlist(db, user_id)


@router.delete("/{ticker}")
def remove_ticker(ticker: str, db: Session = Depends(get_db), 
					user_id: int = Depends(get_current_user_id)):
	service.remove_ticker(db, user_id, ticker)
	return