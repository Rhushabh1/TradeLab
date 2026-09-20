from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.dependencies import get_current_user_id
from app.schemas.notes import NoteCreate, NoteResponse
from app.services.notes_service import NotesService 


router = APIRouter(prefix = "/notes",
					tags = ["Notes"])
service = NotesService()


@router.post("/", response_model = NoteResponse)
def create_note(body: NoteCreate, db: Session = Depends(get_db),
				user_id: int = Depends(get_current_user_id)):
	return service.create_note(db, user_id, body.ticker, body.content)


@router.get("/", response_model = list[NoteResponse])
def list_notes(db: Session = Depends(get_db),
				user_id: int = Depends(get_current_user_id)):
	return service.list_notes(db, user_id)


@router.get("/{ticker}", response_model = list[NoteResponse])
def list_ticker_notes(ticker: str, db: Session = Depends(get_db),
					user_id: int = Depends(get_current_user_id)):
	return service.list_notes(db, user_id, ticker)


@router.delete("/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db),
				user_id: int = Depends(get_current_user_id)):
	service.delete_note(db, user_id, note_id)
	return