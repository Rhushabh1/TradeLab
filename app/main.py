from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.health import router as health_router
from app.config import settings
from app.logger import logger
from app.api.database import router as db_router


# FastAPI now recommends lifespan mechanism (instead of on_event())
@asynccontextmanager
async def lifespan(app: FastAPI):
	# startup
	logger.info("Application starting...")
	yield
	# shutdown
	logger.info("Application shutting down...")


# main app with APIs
app = FastAPI(title = settings.APP_NAME,
				version = settings.APP_VERSION)


# @app.on_event("startup")
# async def startup():
# 	logger.info("Application starting...")

# @app.on_event("shutdown")
# async def shutdown():
# 	logger.info("Application shutting down...")


# routed health APIs here
app.include_router(health_router)
app.include_router(db_router)