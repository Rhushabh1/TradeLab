from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from sqlalchemy.orm import Session

from app.config import settings
from app.db.database import get_db
from app.db.models import User
from app.schemas.auth import (RegisterRequest, 
								LoginRequest, 
								TokenResponse)
from app.services.auth_service import AuthService


router = APIRouter(prefix = "/auth")
service = AuthService()
security = HTTPBearer()


@router.post("/register")
def register(request: RegisterRequest,
			db: Session = Depends(get_db)):
	service.register(db, request.email, request.password)
	return {
			"message": "User created"
			}


@router.post("/login", response_model = TokenResponse)
def login(request: LoginRequest,
			db: Session = Depends(get_db)):
	token = service.login(db, request.email, request.password)
	return {
			"access_token": token
			}


# decode my JWT credentials as bearer
# usually replaced by get_current_user() dependency & load user from db
@router.get("/me")
def me(credentials: HTTPAuthorizationCredentials = Depends(security)):
	payload = jwt.decode(credentials.credentials,
						settings.JWT_SECRET,
						algorithms = [settings.JWT_ALGORITHM])
	return {
			"email": payload["sub"]
			}