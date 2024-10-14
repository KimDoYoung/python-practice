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
