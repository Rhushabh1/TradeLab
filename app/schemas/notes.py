from datetime import datetime
from pydantic import BaseModel, ConfigDict


class NoteCreate(BaseModel):
	ticker: str
	content: str


class NoteResponse(BaseModel):
	model_config = ConfigDict(from_attributes = True)

	id: int
	tickers: str
	content: str
	created_at: datetime
	updated_at: datetime