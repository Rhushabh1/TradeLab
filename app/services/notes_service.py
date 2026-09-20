from sqlalchemy.orm import Session

from app.core.exceptions import TradeLabException
from app.db.models import Notes, Watchlist
from app.services.watchlist_service import WatchlistService 


class NotesService:
	# when user saves a note
	def create_note(self, db: Session, user_id: int, ticker: str, content: str):
		ticker = WatchlistService().ticker_watched(db, user_id, ticker)
		content = content.strip()
		# for empty note
		if not content:
			raise TradeLabException("Note content is required")
		note = Notes(user_id = user_id,
					ticker = ticker,
					content = content)
		db.add(note)
		db.commit()
		db.refresh(note)
		return note


	# list all of user's notes
	def list_notes(self, db: Session, user_id: int, ticker: str | None = None):
		if ticker is not None:
			ticker = WatchlistService().ticker_watched(db, user_id, ticker)
			query = (db.query(Notes)
					.filter(Notes.user_id == user_id, 
							Notes.ticker == ticker)
					.order_by(Notes.created_at.desc())
					.all())
		else:
			# return notes for tickers which are in user's watchlist
			query = (db.query(Notes)
					.filter(Notes.user_id == user_id)
					.join(Watchlist, 
							(Watchlist.user_id == Notes.user_id) 
							& (Watchlist.ticker == Notes.ticker),)
					.filter(Watchlist.user_id == user_id)
					.order_by(Notes.created_at.desc())
					.all())
		return query


	# delete user's note in question
	def delete_note(self, db: Session, user_id: int, note_id: int):
		note = (db.query(Notes)
				.filter(Notes.id == note_id,
						Notes.user_id == user_id)
				.first())
		if note is None:
			raise TradeLabException("Note not found", status_code = 404)
		db.delete(note)
		db.commit()



