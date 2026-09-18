from sqlalchemy.orm import Session

from app.db.models import User
from app.utils.security import (hash_password,
								verify_password,
								create_token)
from app.core.exceptions import (TradeLabException)


# only service layer can access the DB
# business logic lives in a service layer
class AuthService:
	def register(self, db: Session, email: str, password: str):
		exists = (db.query(User)
					.filter(User.email == email)
					.first())
		if exists:
			raise TradeLabException("Email already exists")

		user = User(email = email, password_hash = hash_password(password))
		db.add(user)
		db.commit()
		return user

	def login(self, db: Session, email: str, password: str):
		user = self.get_user_by_email(db, email)
		if not user:
			raise TradeLabException("Invalid credential")
		if not verify_password(password, user.password_hash):
			raise TradeLabException("Invalid credentials")
		# return JWT token (valid for 60 minutes)
		return create_token(user.email)

	# to get user_id from email (for services)
	def get_user_by_email(self, db: Session, email: str):
		return (db.query(User)
				.filter(User.email == email)
				.first())