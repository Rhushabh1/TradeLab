from fastapi import APIRouter, status

from app.workers.tasks import (refresh_news, refresh_stock_cache, cleanup_cache)


router = APIRouter(prefix = "/workers",
					tags = ["Workers"])


# 202 because the work is queued & not completed during the HTTP request
@router.post("/news", status_code = status.HTTP_202_ACCEPTED)
def queue_news_refresh():
	task = refresh_news.delay()
	return {
			"task_id": task.id,
			"status": "queued"
			}


@router.post("/stock_cache", status_code = status.HTTP_202_ACCEPTED)
def queue_stock_cache_refresh():
	task = refresh_stock_cache.delay()
	return {
			"task_id": task.id,
			"status": "queued"
			}


@router.post("/cleanup_cache", status_code = status.HTTP_202_ACCEPTED)
def queue_cache_cleanup():
	task = cleanup_cache.delay()
	return {
			"task_id": task.id,
			"status": "queued"
			}