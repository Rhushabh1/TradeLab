from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings


engine = create_engine(settings.DATABASE_URL, 
						echo = settings.DEBUG)

SessionLocal = sessionmaker(bind = engine, 
							autoflush = False, 
							autocommit = False)

# fteching db from local session
def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()