from datetime import datetime
from pydantic import BaseModel, ConfigDict


class CompanyProfileResponse(BaseModel):
	model_config = ConfigDict(from_attributes = True)

	ticker: str
	content: str
	source_filename: str
	updated_at: datetime