from sqlalchemy import asc, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.domain.diary.diary_model import Diary
from app.domain.diary.diary_schema import DiaryRequest, DiaryResponse

class DiaryService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # Create
    async def create_diary(self, diary_data: DiaryRequest) -> DiaryResponse:
        new_diary = Diary(
            ymd=diary_data.ymd,
            content=diary_data.content,
            summary=diary_data.summary
        )
        self.db.add(new_diary)
        await self.db.commit()
        await self.db.refresh(new_diary)
        return DiaryResponse.model_validate(new_diary)

    # Read
    async def get_diary(self, ymd: str) -> DiaryResponse | None:
        result = await self.db.execute(select(Diary).filter(Diary.ymd == ymd))
        diary = result.scalar_one_or_none()  # 일치하는 첫 번째 결과를 가져옴
        if diary:
            return DiaryResponse.model_validate(diary)
        return None

    # Update
    async def update_diary(self, ymd: str, diary_data: DiaryRequest) -> DiaryResponse | None:
        result = await self.db.execute(select(Diary).filter(Diary.ymd == ymd))
        diary = result.scalar_one_or_none()
        if diary:
            diary.content = diary_data.content
            diary.summary = diary_data.summary
            await self.db.commit()
            await self.db.refresh(diary)
            return DiaryResponse.model_validate(diary)
        return None

    # Delete
    async def delete_diary(self, ymd: str) -> bool:
        result = await self.db.execute(select(Diary).filter(Diary.ymd == ymd))
        diary = result.scalar_one_or_none()
        if diary:
            await self.db.delete(diary)
            await self.db.commit()
            return True
        return False

    # Read with pagination, date range, and summary_only option
    async def get_diaries(
        self, start_ymd: str, end_ymd: str, start_index: int, limit: int, order: str, summary_only: bool = False
    ) -> dict:
        sort_order = asc(Diary.ymd) if order == 'asc' else desc(Diary.ymd)

        # 기본 SQL 쿼리 작성
        stmt = (
            select(Diary)
            .where(Diary.ymd >= start_ymd)
            .where(Diary.ymd <= end_ymd)
            .order_by(sort_order)
            .offset(start_index)
            .limit(limit + 1)  # +1을 통해 다음 데이터가 있는지 확인
        )

        result = await self.db.execute(stmt)
        diaries = result.scalars().all()

        next_data_exists = 'Y' if len(diaries) > limit else 'N'
        diaries = diaries[:limit]
        last_index = start_index + len(diaries)

        # summary_only가 True일 경우, summary만 반환하도록 함
        if summary_only:
            data = [{"ymd": diary.ymd, "summary": diary.summary} for diary in diaries]
        else:
            data = [DiaryResponse.model_validate(diary) for diary in diaries]

        return {
            "data": data,
            "next_data_exists": next_data_exists,
            "last_index": last_index
        }