from sqlalchemy.orm import Session

from app.core.exceptions import TradeLabException
from app.logger import logger
from app.config import settings
from app.db.models import CompanyProfile, News, Notes, Watchlist
from app.rag.embedder import embed, embed_many


class RAGService:
	# extract context from all the relevant user info -> watchlist, notes, company profiles, news
	def _accumulate_docs(self, db: Session, user_id: int):
		# which tickers to look out for
		tickers = [r[0] for r in (db.query(Watchlist)
								.filter(Watchlist.user_id == user_id)
								.order_by(Watchlist.ticker.asc())
								.all())]
		if not tickers:
			return []
		# will need all profiles
		profiles = (db.query(CompanyProfile)
					.filter(CompanyProfile.ticker.in_(tickers))
					.all())
		# fetch latest notes only
		notes = (db.query(Notes)
				.filter(Notes.user_id == user_id,
						Notes.ticker.in_(tickers))
				.order_by(Notes.updated_at.desc())
				.limit(100)
				.all())
		# fetch latest news only
		news = (db.query(News)
				.filter(News.ticker.in_(tickers))
				.order_by(News.published_at.desc())
				.limit(100)
				.all())
		# add all of them to docs in a standard format
		docs = [f"""Source: company profile | 
					Ticker: {i.ticker} | 
					File: {i.source_filename}\n{i.content}""" for i in profiles]
		docs.extend(f"""Source: user notes | 
					Ticker: {i.ticker}\n{i.content}""" for i in notes)
		docs.extend(f"""Source: news | 
					Ticker: {i.ticker} | 
					Publisher: {i.publisher} | 
					Title: {i.title}\n{i.link}""" for i in news)
		return docs 


	# context for answering the question
	def retrieve_context(self, db: Session, user_id: int, question: str):
		docs = self._accumulate_docs(db, user_id)
		if not docs:
			return []
		# load the RAG dependencies only when retrieval is requested
		# form of lazy loading
		import faiss
		import numpy as np
		# vectorize the doc embeddings
		vectors = np.asarray(embed_many(docs), dtype = "float32")
		# question embeddings
		query_vector = np.asarray([embed(question)], dtype = "float32")
		# ranking top k matches with the query
		# only relevant vectors pass through
		index = faiss.IndexFlatIP(vectors.shape[1])
		index.add(vectors)
		top_k = min(max(settings.RAG_TOP_K, 1), len(docs))
		_, indices = index.search(query_vector, top_k)
		return [docs[i] for i in indices[0].tolist() if i>=0]



	# def build_index(self, db: Session):
	# 	for file in Path("data/company_profiles").glob("*.txt"):
	# 		add_document(file.read_text())
	# 	notes = db.query(Note).all()
	# 	for note in notes:
	# 		add_document(note.content)
	# 	news = db.query(News).all()
	# 	for article in news:
	# 		add_document(article.title)