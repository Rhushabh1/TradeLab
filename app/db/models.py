from enum import Enum
from datetime import datetime
from sqlalchemy import String, Float, ForeignKey, DateTime, func, Text, Enum as SQLEnum
# for easy mapping of python datatypes to orm
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class User(Base):
	__tablename__ = "users"

	id : Mapped[int] = mapped_column(primary_key = True)
	email : Mapped[str] = mapped_column(String(255), unique = True, nullable = False)
	password_hash : Mapped[str] = mapped_column(String(255), nullable = False)
	# no created_at yet


class Stock(Base):
	__tablename__ = "stocks"
	
	id: Mapped[int] =mapped_column(primary_key = True)
	ticker: Mapped[str] = mapped_column(String(20), unique = True, nullable = False)
	name: Mapped[str] = mapped_column(String(255), nullable = False)
	sector: Mapped[str] = mapped_column(String(100), nullable = True)
	current_price: Mapped[float] = mapped_column(Float, nullable = True)
	# no market cap, PE, etc. (will add later if needed)


class Portfolio(Base):
	__tablename__ = "portfolio"
	
	id: Mapped[int] = mapped_column(primary_key = True)
	user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable = False, index = True)
	ticker: Mapped[str] = mapped_column(String(20), nullable = False)
	quantity: Mapped[int] = mapped_column(default = 0, nullable = False)
	average_price: Mapped[float] = mapped_column(Float, nullable = False)


# class TxnType(str, Enum):
# 	BUY = "BUY"
# 	SELL = "SELL"
class Transaction(Base):
	__tablename__ = "transactions"
	
	id: Mapped[int] = mapped_column(primary_key = True)
	user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable = False, index = True)
	ticker: Mapped[str] = mapped_column(String(20), nullable = False)
	transaction_type: Mapped[str] = mapped_column(String(10), nullable = False)
	quantity: Mapped[int] = mapped_column(nullable = False)
	price: Mapped[float] = mapped_column(Float, nullable = False)
	# time is important here
	created_at: Mapped[datetime] = mapped_column(DateTime(), server_default = func.now())


class News(Base):
	__tablename__ = "news"
	
	id: Mapped[int] = mapped_column(primary_key = True)
	ticker: Mapped[str] = mapped_column(String(20), nullable = False)
	title: Mapped[str] = mapped_column(String(500))
	publisher: Mapped[str] = mapped_column(String(100))
	link: Mapped[str] = mapped_column(String(1000))
	published_at: Mapped[datetime] = mapped_column(DateTime(), server_default = func.now())
	# not storing content/summaries/embeddings yet


# TODO - add ondelete feature for cascading deletes
class Watchlist(Base):
	__tablename__ = "watchlist"

	id: Mapped[int] = mapped_column(primary_key = True)
	user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable = False, index = True)
	ticker: Mapped[str] = mapped_column(String(20), ForeignKey("stocks.ticker"), nullable = False)
	# no created_at yet


class Notes(Base):
	__tablename__ = "notes"
	
	id: Mapped[int] = mapped_column(primary_key = True)
	user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable = False, index = True)
	ticker: Mapped[str] = mapped_column(String(20), ForeignKey("stocks.ticker"), nullable = False)
	# to avoid empty notes spamming table
	content: Mapped[str] = mapped_column(Text, nullable = False)
	# for proper versioning (user can edit same note on a ticker)
	created_at: Mapped[datetime] = mapped_column(DateTime(), server_default = func.now())
	updated_at: Mapped[datetime] = mapped_column(DateTime(), server_default = func.now(), onupdate = func.now())


class CompanyProfile(Base):
	__tablename__ = "company_profiles"

	id: Mapped[int] = mapped_column(primary_key = True)
	ticker: Mapped[str] = mapped_column(String(20), ForeignKey("stocks.ticker"), unique = True, nullable = False)
	content: Mapped[str] = mapped_column(Text)
	source_filename: Mapped[str] = mapped_column(String(255), nullable = False)
	# to prevent rewriting
	updated_at: Mapped[datetime] = mapped_column(DateTime(), server_default = func.now(), onupdate = func.now())


# class AIStatus(str, Enum):
# 	QUEUED = "QUEUED"
# 	PROCESSING = "PROCESSING"
# 	COMPLETED = "COMPLETED"
# 	FAILED = "FAILED"
class AIRequest(Base):
	__tablename__ = "ai_requests"
	
	id: Mapped[str] = mapped_column(String(50), primary_key = True)
	user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable = False, index = True)
	question: Mapped[str] = mapped_column(Text, nullable = False)
	answer: Mapped[str | None] = mapped_column(Text)
	status: Mapped[str] = mapped_column(String(20), nullable = False)
	# for computing latency
	created_at: Mapped[datetime] = mapped_column(DateTime(), server_default = func.now())
	updated_at: Mapped[datetime] = mapped_column(DateTime(), server_default = func.now(), onupdate = func.now())