# scheduler_routes.py
from fastapi import APIRouter, HTTPException
from backend.app.core.scheduler import Scheduler
from backend.app.domains.system.job_model import JobRequest
from backend.app.scheduler.schedule_mapping import task_mapping

router = APIRouter()

@router.get("/")
def get_jobs():
    ''' 스케줄러 job 목록 조회 '''
    scheduler = Scheduler.get_instance()
    jobs = scheduler.get_jobs()
    return [{"id": job.id, "name": job.name, "next_run_time": str(job.next_run_time)} for job in jobs]


@router.post("/add")
def add_job(job_request: JobRequest):
    scheduler = Scheduler.get_instance()
    try:
        task_name = job_request.task_name
        job_id = job_request.job_id
        args = tuple(job_request.args)
        run_type = job_request.run_type

        task_func = task_mapping.get(task_name)
        if task_func is None:
            raise HTTPException(status_code=400, detail="Task not found")

        if run_type == "date":
            if job_request.run_date is None:
                raise HTTPException(status_code=400, detail="run_date must be provided for date jobs")
            run_date = job_request.run_date
            scheduler.add_date_job(task_func, run_date=run_date, job_id=job_id, args=args)
        elif run_type == "cron":
            if job_request.cron is None:
                raise HTTPException(status_code=400, detail="cron must be provided for cron jobs")
            cron_expression = job_request.cron
            scheduler.add_cron_job(task_func, cron_expression, job_id, args)
        else:
            raise HTTPException(status_code=400, detail="Invalid run_type")
        
        return {"message": "Job added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    

@router.delete("/remove/{job_id}")
def remove_job(job_id: str):
    scheduler = Scheduler.get_instance()
    try:
        scheduler.remove_job(job_id)
        return {"message": "Job removed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
