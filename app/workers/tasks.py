from app.logger import logger
from app.workers.celery_app import celery
from app.cache.cache_service import cache 
from app.db.database import SessionLocal
from app.services.stock_service import StockService 
from app.workers.task_history import task_history


RETRY_BACKOFF_MAX = 300
MAX_RETRIES = 3

def _record_history(task_name: str, task_id: str | None, status: str, details):
	try:
		task_history.record(task_name, task_id, status, details)
	except Exception:
		logger.exception(f"Failed to record task history for {task_name}")


# async tasks -> executed by celery worker after APScheduler dispatches it
# create own db session -> business logic -> record outcome -> close session
@celery.task(bind = True,
			name = "app.workers.tasks.refresh_stock_cache",
			autoretry_for = (Exception,),
			retry_backoff = True,
			retry_backoff_max = RETRY_BACKOFF_MAX,
			retry_jitter = True,
			retry_kwargs = {"max_retries": MAX_RETRIES})
def refresh_stock_cache(self):
	# self is for celery task
	logger.info("Refreshing stock cache...")
	db = SessionLocal()
	task_id = self.request.id
	try:
		result = StockService().refresh_stock_prices(db)
	except Exception as e:
		_record_history("refresh_stock_cache", task_id, "FAILURE", {"error": str(e)})
		raise
	finally:
		db.close()
	_record_history("refresh_stock_cache", task_id, "SUCCESS", result)
	return result


@celery.task(bind = True,
			name = "app.workers.tasks.cleanup_cache",
			autoretry_for = (Exception,),
			retry_backoff = True,
			retry_backoff_max = RETRY_BACKOFF_MAX,
			retry_jitter = True,
			retry_kwargs = {"max_retries": MAX_RETRIES})
def cleanup_cache(self):
	logger.info("Cleaning cache...")
	task_id = self.request.id 
	try:
		deleted = cache.cleanup_keys_without_ttl()
	except Exception as e:
		_record_history("cleanup_cache", task_id, "FAILURE", {"error": str(e)})
		raise
	result = {"deleted_keys": deleted}
	_record_history("cleanup_cache", task_id, "SUCCESS", result)
	return result


# TODO - placeholder for news refresh
@celery.task(bind = True,
			name = "app.workers.tasks.refresh_news")
def refresh_news(self):
	logger.info("Refreshing news...")
	db = SessionLocal()
	task_id = self.request.id
	try:
		result = NewsService().refresh_news(db)
	except Exception as e:
		_record_history("refresh_news", task_id, "FAILURE", {"error": str(e)})
		raise
	finally:
		db.close()
	_record_history("refresh_news", task_id, "SUCCESS", result)
	return result