from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.config import settings
from app.core.exceptions import TradeLabException
from app.db.database import get_db
from app.db.models import User
from app.services.auth_service import AuthService


# catches swagger UI "Authorize" as bearer
security = HTTPBearer(auto_error = False)
# doesn't query the users table directly
service = AuthService()


# reusable dependency (lives outside service layers & security utilities)
# returns complete authenticated User object
def get_current_user(credentials: HTTPAuthorizationCredentials | None = Depends(security),
					db: Session = Depends(get_db)) -> User:
	if credentials is None:
		raise TradeLabException("Authentication required", status_code = 401)
	try:
		payload = jwt.decode(credentials.credentials,
							settings.JWT_SECRET,
							algorithms = [settings.JWT_ALGORITHM])
	except JWTError:
		raise TradeLabException("Invalid or expired token", status_code = 401)
	email = payload.get("sub")
	if not isinstance(email, str) or not email:
		raise TradeLabException("Invalid token", status_code = 401)
	user = service.get_user_by_email(db, email)
	if user is None:
		raise TradeLabException("Invalid or expired token", status_code = 401)
	return user 


# use in APIs which need an authenticated identity
def get_current_user_id(user: User = Depends(get_current_user)) -> int:
	return user.id
