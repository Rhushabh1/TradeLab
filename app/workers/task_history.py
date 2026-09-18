import json
from datetime import datetime, timezone

from app.cache.redis_client import client 


HISTORY_KEY = "tradelab:scheduler:history"
MAX_HISTORY = 20


# redis backed history service without adding db table
# history reads from redis (so both API & Celery see the same task records)
class TaskHistory:
	def record(self, task_name: str, task_id: str | None, status: str, details: dict | None = None):
		entry = {
				"task_name": task_name,
				"task_id": task_id,
				"status": status,
				"timestamp": datetime.now(timezone.utc).isoformat(),
				"details": details or {}
				}
		client.lpush(HISTORY_KEY, json.dumps(entry))
		# keeps most recent 20 task records
		client.ltrim(HISTORY_KEY, 0, MAX_HISTORY - 1)

	def get_recent(self):
		entries = client.lrange(HISTORY_KEY, 0, MAX_HISTORY - 1)
		return [json.loads(entry) for entry in entries]


task_history = TaskHistory()