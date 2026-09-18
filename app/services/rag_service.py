from sqlalchemy.orm import Session

from app.core.exceptions import TradeLabException
from app.logger import logger
from app.cache.cache_service import cache 
from app.rag.vector_store import add_document


class RAGService:
	def build_index(self, db: Session):
		for file in Path("data/company_profiles").glob("*.txt"):
			add_document(file.read_text())
		notes = db.query(Note).all()
		for note in notes:
			add_document(note.content)
		news = db.query(News).all()
		for article in news:
			add_document(article.title)