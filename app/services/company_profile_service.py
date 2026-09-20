from pathlib import Path 
from sqlalchemy.orm import Session

from app.config import settings
from app.core.exceptions import TradeLabException
from app.db.models import CompanyProfile, Watchlist
from app.services.watchlist_service import WatchlistService
from app.services.stock_service import StockService


class CompanyProfileService:
	# returns profile path of ticker in the directory
	def _profile_path(self, ticker: str):
		profile_dir = Path(settings.COMPANY_PROFILE_DIR)
		# TODO - handle suffix issue for some company profiles
		path = profile_dir / f"{ticker}.txt"
		if path.is_file():
			return path 
		return None


	# syncs up db with profile from the file
	def sync_profile_from_file(self, db: Session, ticker: str):
		path = self._profile_path(ticker)
		if path is None:
			return None
		content = path.read_text().strip()
		if not content:
			return None
		# ensure stock exists in db before saving its profile
		StockService().get_stock(db, ticker)
		profile = (db.query(CompanyProfile)
					.filter(CompanyProfile.ticker == ticker)
					.first())
		# if profile doesn't exist in db
		if profile is None:
			profile = CompanyProfile(ticker = ticker,
									content = content,
									source_filename = path.name)
			db.add(profile)
		else:
			profile.content = content
			profile.source_filename = path.name
		db.commit()
		db.refresh(profile)
		return profile


	# fetches profile if it is in watchlist
	def get_profile(self, db: Session, user_id: int, ticker: str):
		# check if in the watchlist
		ticker = WatchlistService().ticker_watched(db, user_id, ticker)
		profile = (db.query(CompanyProfile)
					.filter(CompanyProfile.ticker == ticker)
					.first())
		# fetch from file if not in db
		if profile is None:
			profile = self.sync_profile_from_file(db, ticker)
		# if no local file available
		if profile is None:
			raise TradeLabException(f"No local company profile is available for {ticker}", status_code = 404)
		return profile
