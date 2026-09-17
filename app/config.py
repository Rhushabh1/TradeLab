# added config mgmt early so future features don't hardcode values
from pydantic_settings import BaseSettings, SettingsConfigDict


# matches with ".env.example" file settings
class Settings(BaseSettings):
	APP_NAME : str = "TradeLab"
	APP_VERSION : str = "0.1.0"
	DEBUG : bool = True
	HOST : str = "0.0.0.0"
	PORT : int = 8000
	# new pydantic v3 style
	model_config = SettingsConfigDict(env_file = ".env")

	DATABASE_URL: str


settings = Settings()