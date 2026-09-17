from fastapi import APIRouter


router = APIRouter()

# basic API health endpoint
# standard readiness practice
@router.get("/health")
def health():
	return {"status" : "healthy"}

# homepage routing
@router.get("/")
def root():
	return {"application" : "TradeLab",
			"message" : "Welcome to TradeLab API"}