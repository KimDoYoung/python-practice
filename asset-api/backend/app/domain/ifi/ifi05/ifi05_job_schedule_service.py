# ifi05_job_schedule_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.app.domain.ifi.ifi05.ifi05_job_schedule_model import Ifi05JobSchedule
from backend.app.domain.ifi.ifi05.ifi05_job_scheduler_schema import (
    Ifi05JobScheduleCreate,
    Ifi05JobScheduleUpdate,
    Ifi05JobScheduleResponse
)
from typing import List
from fastapi import HTTPException, status

class Ifi05JobScheduleService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # 작업 스케줄 생성
    async def create_job_schedule(self, job_data: Ifi05JobScheduleCreate) -> Ifi05JobScheduleResponse:
        new_job = Ifi05JobSchedule(**job_data.dict())
        self.db.add(new_job)
        await self.db.commit()
        await self.db.refresh(new_job)
        return Ifi05JobScheduleResponse.from_orm(new_job)

    # ID로 작업 스케줄 조회
    async def get_job_schedule(self, job_id: int) -> Ifi05JobScheduleResponse:
        result = await self.db.execute(select(Ifi05JobSchedule).where(Ifi05JobSchedule.ifi05_job_schedule_id == job_id))
        job = result.scalar_one_or_none()
        if not job:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job schedule not found")
        return Ifi05JobScheduleResponse.from_orm(job)

    # 모든 작업 스케줄 조회 (페이지네이션)
    async def get_all_job_schedules(self, skip: int = 0, limit: int = 10) -> List[Ifi05JobScheduleResponse]:
        result = await self.db.execute(select(Ifi05JobSchedule).offset(skip).limit(limit))
        jobs = result.scalars().all()
        return [Ifi05JobScheduleResponse.from_orm(job) for job in jobs]

    # 작업 스케줄 업데이트
    async def update_job_schedule(self, job_id: int, job_data: Ifi05JobScheduleUpdate) -> Ifi05JobScheduleResponse:
        result = await self.db.execute(select(Ifi05JobSchedule).where(Ifi05JobSchedule.ifi05_job_schedule_id == job_id))
        job = result.scalar_one_or_none()
        if not job:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job schedule not found")

        for key, value in job_data.dict(exclude_unset=True).items():
            setattr(job, key, value)

        self.db.add(job)
        await self.db.commit()
        await self.db.refresh(job)
        return Ifi05JobScheduleResponse.from_orm(job)

    # 작업 스케줄 삭제
    async def delete_job_schedule(self, job_id: int) -> None:
        result = await self.db.execute(select(Ifi05JobSchedule).where(Ifi05JobSchedule.ifi05_job_schedule_id == job_id))
        job = result.scalar_one_or_none()
        if not job:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job schedule not found")

        await self.db.delete(job)
        await self.db.commit()
