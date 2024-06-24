import asyncio
from typing import List
from backend.app.core.logger import get_logger

from backend.app.domains.system.scheduler_job_model import SchedulerJob
#from backend.app.background.jobs.job_test import test1
from backend.app.background.schedule_mapping import job_mapping

logger = get_logger(__name__)

#TODO 다듬을 것 DB를 쓸 것인지? 만약 쓰지 않는다면 ... Scheduler instance를 삭제
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

    #TODO DB에서 모두 가져오게끔 수정
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

        # TODO 휴일 가져오는 것도 매달 첫째날 1시에 돌리자
        # site38_work = job_mapping['site38_work']
        # self.scheduler.get_instance().add_cron_job(func=self.run_async_job, cron="40 14 * * 1-5", job_id="site38_work",  args=(site38_work,"커뮤니케이션38 스크랩"), max_instances=2)
        
        # holiday_godata = job_mapping['holiday_godata']
        # self.scheduler.get_instance().add_cron_job(func=self.run_async_job, cron="00 17 * * *", job_id="holiday_godata", args=(holiday_godata,"휴일정보"), max_instances=2)
        

        return {"message": "System jobs registered successfully"}