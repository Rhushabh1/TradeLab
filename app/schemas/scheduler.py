from datetime import datetime
from pydantic import BaseModel


# APScheduler jobs have only these useful fields
class JobResponse(BaseModel):
	id: str
	name: str
	trigger: str
	next_run_time: datetime | None = None