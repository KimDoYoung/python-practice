from backend.app.core.logger import get_logger
from motor.motor_asyncio import AsyncIOMotorClient

from backend.app.domains.system.scheduler_job_model import SchedulerJob
from backend.app.background.jobs.job_test import test1

logger = get_logger(__name__)


class SchedulerJobService:
    # _instance = None
    def __init__(self, scheduler):
        self.scheduler = scheduler

    async def create(self, keyvalue: dict):
        scheduler_job = SchedulerJob(**keyvalue)
        await scheduler_job.create()
        return scheduler_job

    async def get_schedule_list(self) -> list[dict]:
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
    
    async def get_all(self) -> list[SchedulerJob]:
        ''' SchedulerJob Collection에서 모든 document를 가져온다.'''
        try:
            scheduler_jobs = await SchedulerJob.find().to_list()
            return scheduler_jobs
        except Exception as e:
            logger.error(f"Failed to retrieve all SchedulerJobs: {e}")
            raise e
    
    async def get_job(self, job_id: str) -> SchedulerJob:
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
    
    async def register_system_jobs(self):
        ''' 
            1. DB에 system jobs 등록 
            2. db에서 모두 읽어서 그것들을  스케줄러에 등록 
        '''
        # 1. DB에 system jobs 등록
        logger.info("1. DB에 system jobs 등록: 없으면 추가 있으면 pass")
        test_job = SchedulerJob.find_one({"job_id": "test_job"})
        count = await test_job.count()
        if count == 0:
            test_Job = SchedulerJob(job_id="test_job", job_name="test1", job_type="system", run_type="cron", func_name="test1", cron="*/5 * * * *", args=["Hello, World!"])
            await test_Job.insert()
        #2. db에서 모두 읽어서 그것들을  스케줄러에 등록
        logger.info("2. DB에서 모두 읽어서 등록")
        self.scheduler.add_cron_job(func=test1, cron="* * * * *", job_id="test_job", job_type="cron", args=["Hello, World!"])
        
        return {"message": "System jobs registered successfully"}