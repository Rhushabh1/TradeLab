from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config import settings
from app.db.database import get_db
from app.db.models import User
from app.schemas.auth import (RegisterRequest, 
								LoginRequest, 
								TokenResponse)
from app.services.auth_service import AuthService
from app.api.dependencies import get_current_user


router = APIRouter(prefix = "/auth",
					tags = ["Auth"])
service = AuthService()


@router.post("/register")
def register(request: RegisterRequest,
			db: Session = Depends(get_db)):
	service.register(db, request.email, request.password)
	return {
			"message": "User created"
			}


# paste this token in "Authorize" Swagger UI
@router.post("/login", response_model = TokenResponse)
def login(request: LoginRequest,
			db: Session = Depends(get_db)):
	# JWT access token generated
	token = service.login(db, request.email, request.password)
	return {
			"access_token": token
			}


# decode my JWT credentials as bearer
# with HTTPBearer security scheme, swagger UI prompts for access token and attach it to protected requests
@router.get("/me")
def me(user: User = Depends(get_current_user)):
	return {
			"id": user.id,
			"email": user.email
			}