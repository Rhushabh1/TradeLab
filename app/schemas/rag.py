from pydantic import BaseModel


class RAGRequest(BaseModel):
	question: str


class RAGResponse(BaseModel):
	documents: list[str]