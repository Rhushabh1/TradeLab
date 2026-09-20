# added config mgmt early so future features don't hardcode values
from pydantic_settings import BaseSettings, SettingsConfigDict


# matches with ".env.example" file settings
class Settings(BaseSettings):
	APP_NAME : str = "TradeLab"
	APP_VERSION : str = "0.1.0"
	DEBUG : bool = True
	HOST : str = "0.0.0.0"
	PORT : int = 8000

	DATABASE_URL: str

	JWT_SECRET : str
	JWT_ALGORITHM : str = "HS256"
	TOKEN_EXPIRE_MINUTES : int = 60

	REDIS_URL : str

	# openai & kafka config
	OPENAI_API_KEY : str | None = None
	OPENAI_MODEL : str = "gpt-4o-mini"
	KAFKA_BOOTSTRAP_SERVERS : str = "kafka:9092"
	KAFKA_AI_TOPIC : str = "ai.requests"
	KAFKA_AI_GROUP_ID : str = "tradelab-ai-worker"

	COMPANY_PROFILE_DIR : str = "data/company_profiles"
	RAG_TOP_K : int = 5
	MODEL_NAME : str = "all-MiniLM-L6-v2"

	model_config = SettingsConfigDict(env_file = ".env",
										env_file_encoding = "utf-8")


settings = Settings()