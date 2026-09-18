from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.dependencies import get_current_user_id
from app.schemas.portfolio import BuyRequest
from app.services.portfolio_service import NotesService 


router = APIRouter(prefix = "/notes",
					tags = ["Notes"])

service = NotesService()


# all the heavy-lifting done by the portfolioservice
@router.post("/", response_model = BuyRequest)
def add_notes(ticker: str, quantity: int, db: Session = Depends(get_db),
	user_id: int = Depends(get_current_user_id)):
	return service.buy(db, user_id)


@router.get("/{ticker}", response_model = )
def fetch_notes():
	pass