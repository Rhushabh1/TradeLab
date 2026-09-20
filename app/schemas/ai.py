from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


AIStatus = Literal["QUEUED", "PROCESSING", "COMPLETED", "FAILED"]


class AIQuestion(BaseModel):
	question: str


class AIRequest(BaseModel):
	request_id: str
	status: AIStatus
	created_at: datetime


class AIResponse(BaseModel):
	model_config = ConfigDict(from_attributes = True)

	id: str
	question: str
	answer: str | None
	status: AIStatus
	created_at: datetime
	updated_at: datetime