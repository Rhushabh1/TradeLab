from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.health import router as health_router
from app.config import settings
from app.logger import logger
from app.api.database import router as db_router
from app.core.middleware import RequestMiddleware
from app.core.exceptions import (TradeLabException,
								tradelab_exception_handler,
								generic_exception_handler)
from app.api.auth import router as auth_router
from app.api.cache import router as cache_router
from app.api.stocks import router as stock_router
from app.api.portfolio import router as portfolio_router
from app.scheduler.scheduler import scheduler
from app.api.scheduler import router as scheduler_router


# FastAPI now recommends lifespan mechanism (instead of on_event())
@asynccontextmanager
async def lifespan(app: FastAPI):
	# startup
	logger.info("Application starting...")
	scheduler.start()
	yield
	# shutdown
	logger.info("Application shutting down...")
	scheduler.shutdown()


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
app.include_router(auth_router)
app.include_router(cache_router)
app.include_router(stock_router)
app.include_router(portfolio_router)
app.include_router(scheduler_router)

# register middleware
app.add_middleware(RequestMiddleware)
# register exception handlers
app.add_exception_handler(TradeLabException, tradelab_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)