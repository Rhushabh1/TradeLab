from apscheduler.schedulers.background import BackgroundScheduler

from app.workers.tasks import (refresh_stock_cache, refresh_news, cleanup_cache)


# APScheduler is lightweight and easy to manage but if horizontally scale
# each instance would execute the same scheduled jobs, leading to duplicates
# need to move scheduling to a dedicated scheduler (celery beat/kubernetes cron job)
scheduler = BackgroundScheduler()

# scheduler no longer executes work -> it dispatches work to celery
# .delay is a shorcut to send it to task manager
# runs every 5 minutes
scheduler.add_job(func = refresh_stock_cache.delay, 
				trigger = "interval",
				minutes = 5, 
				id = "refresh_stock_cache",
				name = "Refresh stock prices and cache",
				replace_existing = True,
				coalesce = True,
				misfire_grace_time = 3600)

# runs every night at midnight 12AM
scheduler.add_job(func = cleanup_cache.delay, 
				trigger = "cron", 
				hour = 0,
				minute = 0,
				id = "cleanup_cache",
				name = "Clean up stock cache",
				replace_existing = True,
				coalesce = True,
				misfire_grace_time = 3600)

# runs every 5 minutes
scheduler.add_job(func = refresh_news.delay, 
				trigger = "interval",
				minutes = 5, 
				id = "refresh_news",
				name = "Refresh news and cache",
				replace_existing = True,
				coalesce = True,
				misfire_grace_time = 3600)