from sqlalchemy import case, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from app.domain.calendar.calendar_model import Calendar  # 위의 SQLAlchemy 모델
from app.domain.calendar.calendar_schema import CalendarRequest, CalendarResponse  # 위의 Pydantic 스키마
from typing import List


class CalendarService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_calendar(self, request: CalendarRequest) -> CalendarResponse:
        ''' 일정 생성 '''
        new_Calendar = Calendar(
            gubun=request.gubun,
            sorl=request.sorl,
            ymd=request.ymd,
            content=request.content
        )
        self.db.add(new_Calendar)
        await self.db.commit()
        await self.db.refresh(new_Calendar)
        return CalendarResponse.model_validate(new_Calendar)

    async def get_1month_calendars(self, yyyymm: str) -> List[CalendarResponse]:
        ''' yyyymm에 해당하는 1개월 일정 목록 조회 
            참고 sql [SELECT 
            id,
            gubun,
            sorl,
            IF(	gubun = 'Y', CONCAT('2024', ymd),
                IF(gubun = 'M', CONCAT('2024', '12', LPAD(ymd, 2, '0')), ymd)
            ) AS ymd,
            content,
            modify_dt
            FROM calendar
            WHERE 
            (gubun IN ('H', 'E') AND ymd LIKE '202412%')
            OR (gubun = 'Y' AND ymd LIKE '12%')
            OR (gubun = 'M' AND ymd BETWEEN '01' AND '31');]
        
        '''
        year = yyyymm[:4]
        month = yyyymm[4:]

        query = select(
            Calendar.id,
            Calendar.gubun,
            Calendar.sorl,
            case(
                (Calendar.gubun == 'Y', func.concat(year, Calendar.ymd)),
                (Calendar.gubun == 'M', func.concat(year, month, func.lpad(Calendar.ymd, 2, '0'))),
                else_=Calendar.ymd
            ).label('ymd'),
            Calendar.content,
            Calendar.modify_dt
        ).where(
            (
                (Calendar.gubun.in_(['H', 'E']) & Calendar.ymd.like(f'{year}{month}%'))
                | ((Calendar.gubun == 'Y') & Calendar.ymd.like(f'{month}%'))
                | ((Calendar.gubun == 'M') & Calendar.ymd.between('01', '31'))
            )
        )

        result = await self.db.execute(query)
        rows = result.all()

        return [CalendarResponse.model_validate(row) for row in rows]
    
    #-------------------------------------------------------------
    async def get_Calendar_by_id(self, Calendar_id: int) -> CalendarResponse:
        result = await self.db.execute(select(Calendar).where(Calendar.id == Calendar_id))
        Calendar = result.scalar_one_or_none()
        if not Calendar:
            raise NoResultFound(f"Calendar with ID {Calendar_id} not found.")
        return CalendarResponse.from_orm(Calendar)

    async def get_all_Calendars(self) -> List[CalendarResponse]:
        result = await self.db.execute(select(Calendar))
        Calendars = result.scalars().all()
        return [CalendarResponse.from_orm(Calendar) for Calendar in Calendars]

    async def update_Calendar(self, Calendar_id: int, request: CalendarRequest) -> CalendarResponse:
        result = await self.db.execute(select(Calendar).where(Calendar.id == Calendar_id))
        Calendar = result.scalar_one_or_none()
        if not Calendar:
            raise NoResultFound(f"Calendar with ID {Calendar_id} not found.")

        Calendar.gubun = request.gubun
        Calendar.sorl = request.sorl
        Calendar.ymd = request.ymd
        Calendar.content = request.content
        await self.db.commit()
        await self.db.refresh(Calendar)
        return CalendarResponse.from_orm(Calendar)

    async def delete_Calendar(self, Calendar_id: int) -> None:
        result = await self.db.execute(select(Calendar).where(Calendar.id == Calendar_id))
        Calendar = result.scalar_one_or_none()
        if not Calendar:
            raise NoResultFound(f"Calendar with ID {Calendar_id} not found.")

        await self.db.delete(Calendar)
        await self.db.commit()
