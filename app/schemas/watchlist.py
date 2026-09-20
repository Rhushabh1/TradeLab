from datetime import datetime
from pydantic import BaseModel, ConfigDict


class WatchlistCreate(BaseModel):
	ticker: str


class WatchlistResponse(BaseModel):
	model_config = ConfigDict(from_attributes = True)

	ticker: str
	# company profile available?