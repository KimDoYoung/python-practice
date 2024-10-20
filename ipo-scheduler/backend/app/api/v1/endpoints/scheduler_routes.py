# scheduler_routes.py
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from backend.app.core.scheduler import Scheduler
from backend.app.domains.system.config_service import DbConfigService
from backend.app.domains.system.scheduler_job_model import JobRequest, SchedulerJob
from backend.app.domains.system.scheduler_job_service import SchedulerJobService
from backend.app.background.schedule_mapping import job_mapping
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

@router.get("/{job_id}")
async def get_1(job_id : str, scheduler_job_servce: SchedulerJobService = Depends(get_scheduler_job_service))-> SchedulerJob:
    ''' 스케줄러 job1개 조회  '''
    job = await scheduler_job_servce.get_1(job_id)
    return job

@router.post("/edit/{job_id}")
async def update_job(job_request: JobRequest, scheduler_job_servce: SchedulerJobService = Depends(get_scheduler_job_service)):
    
    try:
        # DB에 변경사항을 저장하고
        await scheduler_job_servce.update(job_request)
        # 스케줄러에 변경사항을 반영한다.
        await scheduler_job_servce.register_system_jobs()
        
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
    process = job_mapping[program_id]
    if process is None:
        raise HTTPException(status_code=400, detail="Task not found")

    status = await config_service.get_process_status(program_id)
    if status:
        if status.value == 'running':
            raise HTTPException(status_code=400, detail=f"{program_id} is already running")
    
    await config_service.set_process_status({"mode":"System", "key":f"{program_id}", "value":"running", 'note':f'백그라운드 프로세스 {program_id} is running'})
    background_tasks.add_task(process)
        

    return {"detail": f"{program_id} is started successfully"}    