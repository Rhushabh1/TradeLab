from fastapi import APIRouter

from app.scheduler.scheduler import scheduler
from app.scheduler.jobs import history
from app.schemas.scheduler import JobResponse


router = APIRouter(prefix = "/scheduler",
					tags = ["Scheduler"])


@router.get("/jobs", response_model = list[JobResponse])
def jobs():
	return scheduler.get_jobs()


# will record execution history in db
@router.get("/history")
def execution_history():
	return history


# adds job to history
@router.post("/run/{job_id}")
def run(job_id: str):
	job = scheduler.get_job(job_id)
	if not job:
		return {
				"error": "Job not found"
				}
	job.func()
	return {
			"status": "Executed"
			}