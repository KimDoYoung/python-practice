# scheduler_job_service.py
"""
모듈 설명: 
    -   설명을 넣으시오
주요 기능:
    -   기능을 넣으시오

작성자: 김도영
작성일: 2024-11-07
버전: 1.0
"""
import asyncio
from backend.app.core.scheduler import Scheduler
from sqlalchemy import select
from backend.app.domain.ifi.ifi05.ifi05_job_schedule_model import Ifi05JobSchedule  # SQLAlchemy 모델로 가정
from backend.app.background.schedule_mapping import job_mapping
from backend.app.core.logger import get_logger
from backend.app.core.database import get_session

logger = get_logger()

class SchedulerJobService:
    def __init__(self, scheduler: Scheduler):
        # self.db_session = db_session
        self.scheduler = scheduler
        # 이벤트 루프를 명확히 초기화
        try:
            self.loop = asyncio.get_event_loop()
            if self.loop.is_closed():  # 이벤트 루프가 종료된 경우 새로운 루프 생성
                self.loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self.loop)
        except RuntimeError:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)        

    async def get_jobs_from_db(self):
        """DB에서 스케줄 정보를 가져옵니다."""
        async with get_session() as session:
            query = select(Ifi05JobSchedule)
            result = await session.execute(query)
            return result.scalars().all()
        
    async def run_async_task(self, coro):
        return await coro

    def run_async_job(self, coro, *args, **kwargs):
        if not hasattr(self, 'loop') or self.loop.is_closed():
                    self.loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(self.loop)        
        asyncio.run_coroutine_threadsafe(self.run_async_task(coro(*args, **kwargs)), self.loop)          

    async def register_system_jobs(self):
        """DB에서 스케줄 정보를 읽어 scheduler에 등록합니다."""
        jobs = await self.get_jobs_from_db()
        for job in jobs:
            await self.register_job(job)

    async def register_job(self, job_record: Ifi05JobSchedule):
        """단일 스케줄 job을 등록합니다."""
        job_nm = job_record.ifi05_job_schedule_nm
        try:
            # job_mapping에 job_nm이 존재하는지 확인
            job_function = job_mapping[job_nm]
        except KeyError:
            logger.error("------------------------- Error -------------------------")
            logger.error(f"스케줄 JOB 매핑실패(프로세스가 없음): Failed to add job {job_nm}: Job function '{job_nm}' not found in job_mapping")
            logger.error("---------------------------------------------------------")
            return  # 함수가 없을 경우 조기 종료        
        scheduler = self.scheduler.get_instance()
        if job_record.ifi05_run_type == 'cron' and job_record.ifi05_cron_str:
            try:
                job_id = str(job_record.ifi05_job_schedule_id)
                job_nm = job_record.ifi05_job_schedule_nm
                job_function = job_mapping[job_nm]
                job_args = job_record.ifi05_args
                job_cron = job_record.ifi05_cron_str
                # 스케줄에 job 추가
                scheduler.remove_job(job_id)
                scheduler.add_cron_job(func=self.run_async_job, cron=job_cron, job_id=job_id, args=(job_function, job_args), max_instances=2)                
                logger.info(f"Job '{job_nm}' added with cron '{job_id}'")
            except Exception as e:
                logger.error("------------------------- Error -------------------------")
                logger.error(f"스케줄 JOB 등록 실패: Failed to add job {job_record.ifi05_job_schedule_nm}: {e}", exc_info=True)
                logger.error("---------------------------------------------------------")

# 의존성 주입을 통해 scheduler와 db_session을 설정합니다.
# async def get_scheduler_job_service() -> SchedulerJobService:
#     scheduler = Scheduler.get_instance()
#     return SchedulerJobService(scheduler=scheduler)

_scheduler_job_service_instance = None  # 모듈 전역에서 인스턴스를 저장할 변수

async def get_scheduler_job_service() -> SchedulerJobService:
    global _scheduler_job_service_instance
    if _scheduler_job_service_instance is None:
        scheduler = Scheduler.get_instance()
        _scheduler_job_service_instance = SchedulerJobService(scheduler=scheduler)
    return _scheduler_job_service_instance