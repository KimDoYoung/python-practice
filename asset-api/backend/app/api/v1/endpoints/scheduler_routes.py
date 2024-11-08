from typing import Dict, List
from fastapi import APIRouter
from backend.app.core.logger import get_logger
from backend.app.domain.ifi.ifi05.ifi05_job_schedule_schema import Ifi05JobScheduleCreate, Ifi05JobScheduleResponse
from backend.app.domain.ifi.ifi05.ifi05_job_schedule_service import Ifi05Service
from backend.app.core.scheduler import Scheduler
from backend.app.domain.scheduler.scheduler_job_service import get_scheduler_job_service

logger = get_logger()

router = APIRouter()

@router.get("/list", response_model=List[Ifi05JobScheduleResponse])
async def list_schedule():
    """스케줄 목록 조회"""
    scheduler = Scheduler.get_instance()
    list_ifi05 = await Ifi05Service.list_all()
    for ifi05 in list_ifi05:
        job = scheduler.find_job(str(ifi05.ifi05_job_schedule_id))
        if job:
            ifi05.next_run_time = job.next_run_time.strftime("%Y-%m-%d %H:%M:%S")
    
    return list_ifi05

@router.get("/reload", response_model=dict)
async def reload_schedule():
    """스케줄 재등록: 현재 등록된 프로세스 모두제거, Db에서 목록을 읽어서 등록"""
    scheduler = Scheduler.get_instance()
    scheduler.remove_all_jobs()
    scheduler_service = await get_scheduler_job_service()
    await scheduler_service.register_system_jobs()
    logger.info("reload_schedule success")
    return {"message": "success"}

@router.get("/get/{id}", response_model=Ifi05JobScheduleResponse)
async def get_schedule(id:int):
    """스케줄 목록 조회"""
    ifi05 = await Ifi05Service.get_1(id)
    
    return ifi05

@router.post("/insert", response_model=Dict[str, str])
async def add_schedule(request: Ifi05JobScheduleCreate):
    """스케줄 목록 추가"""
    await Ifi05Service.create(request)
    return {"message": "success"}
    
@router.put("/update", response_model=Dict[str, str])
async def add_schedule(request: Ifi05JobScheduleResponse):
    """스케줄 목록 수정"""
    await Ifi05Service.update(request)
    return {"message": "success"}

@router.delete("/delete/{id}", response_model=Ifi05JobScheduleResponse)
async def delete_schedule(id:int):
    """스케줄 목록 삭제"""
    ifi05 = await Ifi05Service.delete(id)
    return Ifi05JobScheduleResponse.model_validate(ifi05)
    
    