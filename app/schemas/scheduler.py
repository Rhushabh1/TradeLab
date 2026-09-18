from datetime import datetime
from pydantic import BaseModel, ConfigDict


class JobResponse(BaseModel):
	# construct response schema from object's attributes, rather than a dictionary
	model_config = ConfigDict(from_attributes = True)

	id: int
	name: str
	status: str
	created_at: datetime