from sqlalchemy import String
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