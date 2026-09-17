from fastapi import APIRouter
# testing custom exceptions
from app.core.exceptions import TradeLabException


router = APIRouter()

# basic API health endpoint
# standard readiness practice
@router.get("/health")
def health():
	return {
			"status": "healthy"
			}

# homepage routing
@router.get("/")
def root():
	return {
			"application": "TradeLab",
			"message": "Welcome to TradeLab API"
			}

@router.get("/error")
def error():
	raise TradeLabException("Example custom exception")