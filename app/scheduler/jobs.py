from datetime import datetime


# collection of tasks -> to call services later
history = []


def record(job):
	history.append({
					"job": job,
					"time": datetime.utcnow()
					})
	# only keeping last 20 jobs
	history[:] = history[-20:]


def refresh_stock_cache():
	print("Refreshing stock cache...")
	record("refresh_stock_cache")


def refresh_news():
	print("Refreshing news...")
	record("refresh_news")


def cleanup_cache():
	print("Cleaning cache...")
	record("cleanup_cache")