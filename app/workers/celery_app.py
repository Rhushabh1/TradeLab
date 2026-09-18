from celery import Celery 

from app.config import settings


# TODO - add retry logic (max retries, exponential backoff)
# 
celery = Celery("tradelab",
				broker = settings.REDIS_URL,
				backend = settings.REDIS_URL)

celery.autodiscover_tasks(["app.workers"])