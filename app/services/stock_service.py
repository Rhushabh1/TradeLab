import yfinance as yf 
from sqlalchemy.orm import Session

from app.cache.cache_service import cache 
from app.db.models import Stock


# cache-aside pattern

# why save to db? ->
# persisting stock metadata gives us local availability if yfinance slow/unavailable
# to enrich records later (notes, tags, AI summaries)
# reduced dependence on external APIs
class StockService:
	def get_stock(self, db: Session, ticker: str):
		key = f"stock:{ticker}"
		cached = cache.get(key)
		# cache HIT
		if cached:
			return cached
		# cache MISS -> fetch db -> add to cache
		stock = (db.query(Stock)
				.filter(Stock.ticker == ticker.upper())
				.first())
		# db HIT -> add to cache
		if stock:
			data = {
					"ticker": stock.ticker,
					"name": stock.name,
					"sector": stock.sector,
					"current_price": stock.current_price
					}
			cache.set(key, data, ttl=600)
			return data
		# db MISS -> fetch yfinance -> add to db -> add to cache
		info = yf.Ticker(ticker).info
		data = {
				"ticker": ticker.upper(),
				"name": info.get("longName"),
				"sector": info.get("sector"),
				"current_price": info.get("currentPrice")
				}
		db_stock = Stock(**data)
		db.add(db_stock)
		db.commit()
		cache.set(key, data, ttl=600)
		return data