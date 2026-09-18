from fastapi import APIRouter, status

from app.scheduler.scheduler import scheduler
from app.schemas.scheduler import JobResponse
from app.workers.task_history import task_history
from app.core.exceptions import TradeLabException


router = APIRouter(prefix = "/scheduler",
					tags = ["Scheduler"])


# should be able to serialize the Job object
@router.get("/jobs", response_model = list[JobResponse])
def jobs():
	return [{
			"id": job.id,
			"name": job.name,
			"next_run_time": getattr(job, "next_run_time", None),
			"trigger": str(job.trigger)
			}
			for job in scheduler.get_jobs()]


# TODO - record execution history in db
@router.get("/history")
def execution_history():
	return task_history.get_recent()


# adds job to history
# dispatches a task and returns its task_id -> doesn't wait for background task to finish
@router.post("/run/{job_id}", status_code = status.HTTP_202_ACCEPTED)
def run(job_id: str):
	job = scheduler.get_job(job_id)
	if job is None:
		raise TradeLabException("Job not found", 404)

	# scheduled functions are celery .delay callables
	task = job.func()
	return {
			"status": "QUEUED",
			"task_id": getattr(task, "id", None)
			}