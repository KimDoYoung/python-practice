# scheduler_routes.py
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from backend.app.core.scheduler import Scheduler
from backend.app.domains.system.config_service import DbConfigService
from backend.app.domains.system.scheduler_job_model import JobRequest
from backend.app.domains.system.scheduler_job_service import SchedulerJobService
from backend.app.background.schedule_mapping import task_mapping
from backend.app.core.logger import get_logger
from backend.app.core.dependency import get_config_service, get_scheduler_job_service

logger = get_logger(__name__)

router = APIRouter()

@router.get("/")
async def get_jobs(scheduler_job_servce: SchedulerJobService = Depends(get_scheduler_job_service)):
    ''' 스케줄러 job 목록 조회  '''
    job_list = await scheduler_job_servce.get_schedule_list()

    # db_jobs = await scheduler_job_servce.get_all()
    # scheduler = Scheduler.get_instance()
    # scheduler_jobs = scheduler.get_jobs()
    # scheduler_job_ids = {job.id for job in scheduler_jobs}

    # job_list = []
    # for job in db_jobs:
    #     job_dict = job.model_dump()
    #     job_dict["is_running"] = job.job_id in scheduler_job_ids
    #     job_dict["next_run_time"] = str(next((j.next_run_time for j in scheduler_jobs if j.id == job.job_id), None))
    #     job_list.append(job_dict)
    logger.debug(f"job_list: {job_list}")
    return job_list    

@router.post("/add")
async def add_job(job_request: JobRequest, scheduler_job_servce: SchedulerJobService = Depends(get_scheduler_job_service)):
    
    try:
        # Save job to db
        await scheduler_job_servce.create(job_request.model_dump())

        scheduler = Scheduler.get_instance()
        if job_request.run_type == "date":
            func = task_mapping.get(job_request.func_name)
            if func is None:
                raise HTTPException(status_code=400, detail="Task not found")
            args = tuple(job_request.args)
            scheduler.add_date_job(func=func, cron=job_request.cron, job_id=job_request.job_id, job_type=job_request.job_type, args=args)   
        else:
            func = task_mapping.get(job_request.func_name)
            if job_request.run_date is None:
                raise HTTPException(status_code=400, detail="run_date must be provided for date jobs")
            args = tuple(job_request.args)
            scheduler.add_date_job(func=func, run_date=job_request.run_date, job_id=job_request.job_id, job_type=job_request.job_type, args=args)
        return {"message": "Job added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    

@router.delete("/remove/{job_id}")
async def remove_job(job_id: str, scheduler_job_servce: SchedulerJobService = Depends(get_scheduler_job_service)):

    try:
        scheduler = Scheduler.get_instance()
        await scheduler_job_servce.delete(job_id)
        scheduler.remove_job(job_id)
        return {"message": f"Job {job_id} removed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/run/{program_id}")
async def run(program_id: str, background_tasks: BackgroundTasks, config_service: DbConfigService = Depends(get_config_service)):
    ''' 
        테스트로 프로그램을 돌려본다.
        /api/v1/scheduler/run/scrap_judal
    '''
    process = task_mapping[program_id]
    if process is None:
        raise HTTPException(status_code=400, detail="Task not found")

    status = await config_service.get_process_status(program_id)
    if status:
        if status.value == 'running':
            raise HTTPException(status_code=400, detail=f"{program_id} is already running")
    
    await config_service.set_process_status({"mode":"System", "key":f"{program_id}", "value":"running", 'note':f'백그라운드 프로세스 {program_id} is running'})
    background_tasks.add_task(process)
        

    return {"detail": f"{program_id} is started successfully"}    