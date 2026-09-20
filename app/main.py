from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.config import settings
from app.logger import logger
from app.core.middleware import RequestMiddleware
from app.core.exceptions import (TradeLabException,
								tradelab_exception_handler,
								generic_exception_handler)
from app.scheduler.scheduler import scheduler
from app.api.database import router as db_router
from app.api.health import router as health_router
from app.api.auth import router as auth_router
from app.api.cache import router as cache_router
from app.api.stocks import router as stock_router
from app.api.portfolio import router as portfolio_router
from app.api.watchlist import router as watchlist_router
from app.api.company_profile import router as company_profile_router
from app.api.scheduler import router as scheduler_router
from app.api.worker import router as worker_router
from app.api.notes import router as notes_router
from app.api.news import router as news_router
from app.api.rag import router as rag_router
from app.api.ai import router as ai_router


# FastAPI now recommends lifespan mechanism (instead of on_event())
@asynccontextmanager
async def lifespan(app: FastAPI):
	# startup
	logger.info("Application starting...")
	scheduler.start()
	try: 
		yield
	finally:
		# shutdown
		logger.info("Application shutting down...")
		if scheduler.running: 
			scheduler.shutdown(wait = False)


# main app with APIs
app = FastAPI(title = settings.APP_NAME,
				version = settings.APP_VERSION,
				lifespan = lifespan)


# @app.on_event("startup")
# async def startup():
# 	logger.info("Application starting...")

# @app.on_event("shutdown")
# async def shutdown():
# 	logger.info("Application shutting down...")


# routed APIs here
for router in (db_router,
				health_router,
				auth_router,
				cache_router,
				stock_router,
				portfolio_router,
				watchlist_router,
				company_profile_router,
				scheduler_router,
				worker_router,
				notes_router,
				news_router,
				rag_router,
				ai_router
				):
	app.include_router(router)

# register middleware
app.add_middleware(RequestMiddleware)
# register exception handlers
app.add_exception_handler(TradeLabException, tradelab_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)