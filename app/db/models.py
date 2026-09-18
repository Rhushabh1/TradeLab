from datetime import datetime
from sqlalchemy import String, Float, ForeignKey, DateTime, func
# for easy mapping of python datatypes to orm
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base import Base


class User(Base):
	__tablename__ = "users"
	id : Mapped[int] = mapped_column(primary_key = True)
	email : Mapped[str] = mapped_column(String(255),
										unique = True,
										nullable = False)
	password_hash : Mapped[str] = mapped_column(String(255), 
												nullable = False)
	# no (created_at) timestamp yet


class Stock(Base):
	__tablename__ = "stocks"
	id: Mapped[int] =mapped_column(primary_key = True)
	ticker: Mapped[str] = mapped_column(String(20),
										unique = True)
	name: Mapped[str] = mapped_column(String(255))
	sector: Mapped[str] = mapped_column(String(100),
										nullable = True)
	current_price: Mapped[float] = mapped_column(Float,
												nullable = True)
	# no market cap, PE, etc. (will add later if needed)


class Portfolio(Base):
	__tablename__ = "portfolio"
	id: Mapped[int] = mapped_column(primary_key = True)
	user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
	ticker: Mapped[str] = mapped_column(String(20))
	quantity: Mapped[int]
	average_price: Mapped[float]


class Transaction(Base):
	__tablename__ = "transactions"
	id: Mapped[int] = mapped_column(primary_key = True)
	user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
	ticker: Mapped[str]
	transaction_type: Mapped[str]
	quantity: Mapped[int]
	price: Mapped[float]
	create_at: Mapped[datetime] = mapped_column(DateTime,
												server_default = func.now())