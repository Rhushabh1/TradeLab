from pydantic import BaseModel


class NewsResponse(BaseModel):
	title: str
	publisher: str
	link: str