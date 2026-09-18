from pydantic import BaseModel


class BuyRequest(BaseModel):
	ticker: str
	quantity: int

class SellRequest(BaseModel):
	ticker: str
	quantity: int