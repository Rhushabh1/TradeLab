from apscheduler.schedulers.background import BackgroundScheduler

from app.scheduler.jobs import (refresh_stock_cache, refresh_news, cleanup_cache)


# scheduler -> calls function
# TODO - scheduler -> celery -> worker

# APScheduler is lightweight and easy to manage but if horizontally scale
# each instance would execute the same scheduled jobs, leading to duplicates
# need to move scheduling to a dedicated scheduler (celery beat/kubernetes cron job)
scheduler = BackgroundScheduler()

# using both interval & cron jobs
scheduler.add_job(refresh_stock_cache, "interval", minutes = 30)
scheduler.add_job(refresh_news, "interval", hours = 1)
scheduler.add_job(cleanup_cache, "cron", hour = 0)