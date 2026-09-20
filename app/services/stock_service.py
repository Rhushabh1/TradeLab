import yfinance as yf 
from sqlalchemy.orm import Session

from app.logger import logger
from app.cache.cache_service import cache 
from app.db.models import Stock, Watchlist
from app.core.exceptions import TradeLabException


STOCK_CACHE_TTL_SECONDS = 600

# cache-aside pattern

# why save to db? ->
# persisting stock metadata gives us local availability if yfinance slow/unavailable
# to enrich records later (notes, tags, AI summaries)
# reduced dependence on external APIs
class StockService:
	# Yahoo Finance -> fetch current stock metadata & usable market price
	def _fetch_market_data(self, ticker: str) -> dict:
		info = yf.Ticker(ticker).info
		price = info.get("currentPrice")
		if price is None:
			price = info.get("regularMarketPrice")
		if price is None:
			raise TradeLabException(f"No current market price available for {ticker}")
		return {
				"ticker": ticker,
				"name": info.get("longName") or info.get("shortName") or ticker,
				"sector": info.get("sector"),
				"current_price": float(price)
				}


	@staticmethod
	def _stock_to_dict(stock: Stock) -> dict:
		return {
				"ticker": stock.ticker,
				"name": stock.name,
				"sector": stock.sector,
				"current_price": stock.current_price
				}

	# cache -> db -> yfinance -> db -> cache
	def get_stock(self, db: Session, ticker: str) -> dict:
		# standard ticker
		ticker = ticker.strip().upper()
		if not ticker:
			raise TradeLabException("Ticker is required")
		# (1) cache HIT
		key = f"stock:{ticker}"
		cached = cache.get(key)
		if cached is not None:
			return cached
		# (2) postgreSQL HIT -> add to cache
		stock = (db.query(Stock)
				.filter(Stock.ticker == ticker)
				.first())
		if stock is not None and stock.current_price is not None:
			data = self._stock_to_dict(stock)
			cache.set(key, data, ttl = STOCK_CACHE_TTL_SECONDS)
			return data
		# (3) fetch from yfinance -> add to db -> add to cache
		try:
			data = self._fetch_market_data(ticker)
		except Exception as e:
			logger.exception(f"Failed to fetch stock data for {ticker}")
			raise TradeLabException(f"Unable to retrieve usable stock data for {ticker}") from e
		# (4) add to db
		if stock is None:
			stock = Stock(**data)
			db.add(stock)
		else:
			stock.name = data["name"]
			stock.sector = data["sector"]
			stock.current_price = data["current_price"]
		try:
			db.commit()
			db.refresh(stock)
		except Exception:
			db.rollback()
			raise 
		# (5) populate redis cache
		cache.set(key, data, ttl = STOCK_CACHE_TTL_SECONDS)
		return data


	# unique tickers watched by atleast 1 user (only those are of concern to us)
	def tracked_tickers(self, db: Session):
		tickers = (db.query(Watchlist.ticker)
					.distinct()
					.order_by(Watchlist.ticker.asc())
					.all())
		return [t[0] for t in tickers]


	# refresh prices for all stocks already stored in db
	def refresh_stock_prices(self, db: Session) -> dict:
		# improved query
		stocks = (db.query(Stock)
					.join(Watchlist, 
						Watchlist.ticker == Stock.ticker)
					.distinct()
					.all())
		updated_data = []
		failed_tickers = []

		for stock in stocks:
			try:
				data = self._fetch_market_data(stock.ticker)
				stock.name = data["name"]
				stock.sector = data["sector"]
				stock.current_price = data["current_price"]
				updated_data.append(data)
			except Exception as e:
				logger.exception(f"Failed to refresh price for {ticker}")
				failed_tickers.append(ticker)
		try:
			db.commit()
		except Exception:
			db.rollback()
			raise
		# cache the successfully refreshed prices
		for data in updated_data:
			cache.set(f"stock:{data['ticker']}", data, ttl = STOCK_CACHE_TTL_SECONDS)
		return {
				"updated": len(updated_data),
				"failed": len(failed_tickers),
				"updated_tickers": [data["ticker"] for data in updated_data],
				"failed_tickers": failed_tickers
				}