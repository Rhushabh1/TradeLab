import yfinance as yf 
from sqlalchemy.orm import Session

from app.logger import logger
from app.db.models import News
from app.cache.cache_service import cache
from app.services.stock_service import StockService
from app.core.exception import TradeLabException


NEWS_CACHE_TTL_SECONDS = 600
MAX_NEWS_ARTICLES = 10

# TODO - add caching (use cache_service)
# cache -> db -> yfinance
class NewsService:
	@staticmethod
	def _news_to_dict(news: News) -> dict:
		return {
				"ticker": news.ticker,
				"title": news.title,
				"publisher": news.publisher,
				"link": news.link
				}

	@staticmethod
	def _extract_article_data(article: dict):
		content = article.get("content", article)
		link = content.get("canonicalUrl", {}).get("url") or content.get("link")
		if not link:
			return None
		return {
				"title": content.get("title", ""), 
				"publisher": content.get("provider", {}).get("displayName") or content.get("publisher", ""),
				"link": link
				}

	# fetches directly from yfinance -> db -> cache
	def fetch_news(self, db: Session, ticker: str):
		ticker = ticker.strip().upper()
		if not ticker:
			raise TradeLabException("Ticker is required")
		try:
			articles = yf.Ticker(ticker).news() or []
		except Exception as e:
			logger.exception(f"Failed to fetch news for {ticker}")
			raise TradeLabException(f"Unable to retrieve news for {ticker}") from e
		articles = articles[:MAX_NEWS_ARTICLES]:
		existing_news = (db.query(News)
						.filter(News.ticker == ticker)
						.all())
		existing_by_link = {news.link: news for news in existing_news if news.link}
		results_by_link = {}
		db_changed = False 
		for article in articles:
			data = self._extract_article_data(article)
			if data is None:
				continue
			link = data["link"]
			news = existing_by_link.get(link)
			if news is None:
				# insert new article for this ticker
				news = News(ticker = ticker,
							title = data["title"],
							publisher = data["publisher"],
							link = link)
				db.add(news)
				existing_by_link[link] = news
				db_changed = True
			else:
				# update metadata if source has changed
				if (news.title != data["title"] or news.publisher != data["publisher"]):
					news.title = data["title"]
					news.publisher = data["publisher"]
					db_changed = True
			results_by_link[link] = self._news_to_dict(news)
		# add to db
		if db_changed:
			try:
				db.commit()
			except Exception:
				db.rollback()
				raise
		results = list(results_by_link.values())
		# add to cache -> dictionaries/lists
		cache.set(f"news:{ticker}", results, ttl = NEWS_CACHE_TTL_SECONDS)
		return results

	# fetches from news table
	def get_news(self, db: Session, ticker: str):
		# standard ticker
		ticker = ticker.strip().upper()
		if not ticker:
			raise TradeLabException("Ticker is required")
		# (1) cache HIT
		key = f"news:{ticker}"
		cached = cache.get(key)
		if cached is not None:
			return cached
		# (2) postgreSQL HIT -> add to cache
		news = (db.query(News)
				.filter(News.ticker == ticker)
				.all())
		if news:
			results = [self._news_to_dict(article) for article in news]
			cache.set(key, results, ttl = NEWS_CACHE_TTL_SECONDS)
			return results
		# (3) call yfinance -> add to db -> cache
		return self.fetch_news(db, ticker)

	# refresh news for tracked stocks in stocks table
	def refresh_news(self, db: Session):
		tickers = StockService().tracked_tickers(db)
		updated_tickers = []
		failed_tickers = []
		for ticker in tickers:
			try:
				self.fetch_news(db, ticker)
				updated_tickers.append(ticker)
			except Exception as e:
				db.rollback()
				logger.exception(f"Failed to refresh news for {ticker}")
				failed_tickers.append(ticker)
				continue
		return {
				"updated": len(updated_tickers),
				"failed": len(failed_tickers),
				"failed_tickers": failed_tickers
				}