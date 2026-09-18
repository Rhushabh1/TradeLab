from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

from app.config import settings


pwd_context = CryptContext(schemes = ["bcrypt"],
							deprecated = "auto")


# helper functions for auth + password hashing & verification
# password hashing with bcrypt
def hash_password(password: str) -> str:
	return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
	return pwd_context.verify(password, hashed)

# returns JWT tokens (valid for 60 minutes)
# JWT-based stateless authentication
def create_token(email: str) -> str:
	payload = {
		"sub": email,
		"exp": datetime.utcnow() + timedelta(minutes = settings.TOKEN_EXPIRE_MINUTES)
	}
	return jwt.encode(payload, 
						settings.JWT_SECRET, 
						algorithm = settings.JWT_ALGORITHM)