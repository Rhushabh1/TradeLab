from pydantic import BaseModel


# format to be followed for every stock request
class StockResponse(BaseModel):
	ticker: str 
	name: str 
	sector: str | None
	current_price: float | None