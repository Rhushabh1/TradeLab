from sqlalchemy.orm import Session

from app.core.exceptions import TradeLabException
from app.db.models import Watchlist
from app.services.stock_service import StockService


class WatchlistService:
	# when user adds a ticker to be watched
	def add_ticker(self, db: Session, user_id: int, ticker: str):
		ticker = ticker.strip().upper()
		# verify if entry exists or not
		exists = (db.query(Watchlist)
					.filter(Watchlist.user_id == user_id,
							Watchlist.ticker == ticker)
					.first())
		if exists is not None:
			raise TradeLabException(f"{ticker} already exists in your watchlist")
		# ensure stock exists in db before adding (foreign key constraint)
		# this will populate stock table first before adding watchlist entry
		StockService().get_stock(db, ticker)
		entry = Watchlist(user_id = user_id, 
							ticker = ticker)
		db.add(entry)
		db.commit()
		db.refresh(entry)
		return entry


	# lists all tickers watched by the user
	def list_watchlist(self, db: Session, user_id: int):
		data = (db.query(Watchlist)
				.filter(Watchlist.user_id == user_id)
				.order_by(Watchlist.ticker.asc())
				.all())
		return data


	# checks if the ticker is watched by the user (used by other services)
	def ticker_watched(self, db: Session, user_id: int, ticker: str):
		ticker = ticker.strip().upper()
		if not ticker:
			raise TradeLabException("Ticker is required")
		exists = (db.query(Watchlist)
					.filter(Watchlist.user_id == user_id, 
							Watchlist.ticker == ticker)
					.first())
		if exists is None:
			raise TradeLabException("Ticker doesn't exist in your watchlist", status_code = 404)
		return ticker


	# removes ticker from the user's watchlists
	def remove_ticker(self, db: Session, user_id: int, ticker: str):
		ticker = self.ticker_watched(db, user_id, ticker)
		entry = (db.query(Watchlist)
				.filter(Watchlist.user_id == user_id,
						Watchlist.ticker == ticker)
				.first())
		db.delete(entry)
		db.commit()
