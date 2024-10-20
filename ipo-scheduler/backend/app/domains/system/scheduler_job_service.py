# scheduler_job_service.py
"""
모듈 설명: 
    - SchedulerJob Collection에 대한 비즈니스 로직을 처리하는 서비스 클래스
    - Scheduler (BackgroundScheduler)를 이용하여 스케줄러에 등록된 job을 관리한다.
주요 기능:
    - IPO_SCHEDULER_MODE 시작할 때 DB에서 읽어서 스케줄러에 등록
    - Scheduler class와 Db 를 조합하여  정보를 가져오기
    - SchedulerJob Collection을 변경해서 실행시간을 변경시킬 수 있다

작성자: 김도영
작성일: 24
버전: 1.0
"""
import asyncio
from typing import List
from backend.app.core.logger import get_logger

from backend.app.domains.system.scheduler_job_model import SchedulerJob
from backend.app.background.schedule_mapping import job_mapping

logger = get_logger(__name__)

class SchedulerJobService:
    # _instance = None
    def __init__(self, scheduler):
        self.scheduler = scheduler
        self.loop = asyncio.get_event_loop()

    async def create(self, keyvalue: dict):
        scheduler_job = SchedulerJob(**keyvalue)
        await scheduler_job.create()
        return scheduler_job

    async def get_schedule_list(self) -> List[dict]:
        ''' 
            SchedulerJob Collection에서 모든 document를 가져오고 
            sheduler에 등록된 job_id와 running여부와 next_run_time을 추가하여 반환한다.
        '''
        db_jobs = await self.get_all()
        scheduler_jobs = self.scheduler.get_jobs()
        scheduler_job_ids = {job.id for job in scheduler_jobs}

        job_list = []
        for job in db_jobs:
            job_dict = job.model_dump()
            job_dict["is_running"] = job.job_id in scheduler_job_ids
            job_dict["next_run_time"] = str(next((j.next_run_time for j in scheduler_jobs if j.id == job.job_id), None))
            job_list.append(job_dict)

        return job_list    
    
    async def get_all(self) -> List[SchedulerJob]:
        ''' SchedulerJob Collection에서 모든 document를 가져온다.'''
        try:
            scheduler_jobs = await SchedulerJob.find().to_list()
            return scheduler_jobs
        except Exception as e:
            logger.error(f"Failed to retrieve all SchedulerJobs: {e}")
            raise e
    
    async def get_1(self, job_id: str) -> SchedulerJob:
        scheduler_job = await SchedulerJob.find_one(SchedulerJob.job_id == job_id)
        return scheduler_job
    
    async def update(self, update_data: dict) -> SchedulerJob:
        scheduler_job = await SchedulerJob.find_one(SchedulerJob.job_id == update_data.job_id)
        if scheduler_job:
            await scheduler_job.set(update_data)
            await scheduler_job.save()
            return scheduler_job
        else:
            return None
        
    async def delete(self, job_id: str) -> bool:
        scheduler_job = await SchedulerJob.find_one(SchedulerJob.job_id == job_id)
        if scheduler_job:
            await scheduler_job.delete()
            return True
        else:
            return False

    async def run_async_task(self, coro):
        return await coro

    def run_async_job(self, coro, *args, **kwargs):
        asyncio.run_coroutine_threadsafe(self.run_async_task(coro(*args, **kwargs)), self.loop)        

    async def register_system_jobs(self):
        ''' 
            1. db에서 모두 읽어서 그것들을  스케줄러에 등록 
            2. 기존 등록된 job은 삭제하고 다시 등록한다.
        '''
        logger.info("1. DB에서 모두 읽어서 등록")
        db_jobs = await self.get_all()
        scheduler = self.scheduler.get_instance()
        
        for job in db_jobs:
            job_id = job.job_id
            # 기존 job이 있다면 삭제
            scheduler.remove_job(job_id)
            job_process = job_mapping[job_id]
            # scheduler에 등록 
            scheduler.add_cron_job(func=self.run_async_job, cron=job.cron_str, job_id=job_id, args=(job_process, job.args), max_instances=2)

        return {"message": "System jobs registered successfully"}