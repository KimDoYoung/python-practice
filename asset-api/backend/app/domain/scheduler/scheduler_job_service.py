# scheduler_job_service.py
from scheduler import Scheduler
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.app.domain.ifi.ifi05.ifi05_job_schedule_model import Ifi05JobSchedule  # SQLAlchemy 모델로 가정
from backend.app.core.logger import get_logger

logger = get_logger()

class SchedulerJobService:
    def __init__(self, db_session: AsyncSession, scheduler: Scheduler):
        self.db_session = db_session
        self.scheduler = scheduler

    async def get_jobs_from_db(self):
        """DB에서 스케줄 정보를 가져옵니다."""
        async with self.db_session() as session:
            query = select(Ifi05JobSchedule)
            result = await session.execute(query)
            return result.scalars().all()

    async def register_system_jobs(self):
        """DB에서 스케줄 정보를 읽어 scheduler에 등록합니다."""
        jobs = await self.get_jobs_from_db()
        for job in jobs:
            await self.register_job(job)

    async def register_job(self, job_record: Ifi05JobSchedule):
        """단일 스케줄 job을 등록합니다."""
        if job_record.ifi05_run_type == 'cron' and job_record.ifi05_cron_str:
            try:
                # 실행할 함수를 정의해야 합니다. 예: dummy_function
                def job_function():
                    logger.info(f"Running job: {job_record.ifi05_job_schedule_nm}")

                # 스케줄에 job 추가
                self.scheduler.add_cron_job(
                    func=job_function,
                    cron=job_record.ifi05_cron_str,
                    job_id=str(job_record.ifi05_job_schedule_id)
                )
                logger.info(f"Job '{job_record.ifi05_job_schedule_nm}' added with cron '{job_record.ifi05_cron_str}'")
            except Exception as e:
                logger.error(f"Failed to add job {job_record.ifi05_job_schedule_nm}: {e}", exc_info=True)

# 의존성 주입을 통해 scheduler와 db_session을 설정합니다.
async def get_scheduler_job_service(db_session: AsyncSession) -> SchedulerJobService:
    scheduler = Scheduler.get_instance()
    return SchedulerJobService(db_session=db_session, scheduler=scheduler)
