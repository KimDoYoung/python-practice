from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy import delete

from app.models.snote_model import SNote
from app.schemas.snote_schema import SNoteRequest, SNoteResponse

class SNoteService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_snote(self, snote_id: int) -> SNoteResponse:
        """특정 ID로 노트 조회"""
        result = await self.db.execute(select(SNote).where(SNote.id == snote_id))
        snote = result.scalar_one_or_none()
        if not snote:
            raise NoResultFound(f"SNote with ID {snote_id} not found")
        return SNoteResponse.from_orm(snote)

    async def get_snotes(self) -> list[SNoteResponse]:
        """모든 노트 조회"""
        result = await self.db.execute(select(SNote))
        snotes = result.scalars().all()
        return [SNoteResponse.from_orm(snote) for snote in snotes]

    async def create_snote(self, snote_data: SNoteRequest) -> SNoteResponse:
        """노트 생성"""
        snote = SNote(**snote_data.dict())
        self.db.add(snote)
        await self.db.commit()
        await self.db.refresh(snote)
        return SNoteResponse.from_orm(snote)

    async def delete_snote(self, snote_id: int) -> None:
        """노트 삭제"""
        result = await self.db.execute(select(SNote).where(SNote.id == snote_id))
        snote = result.scalar_one_or_none()
        if not snote:
            raise NoResultFound(f"SNote with ID {snote_id} not found")
        
        await self.db.execute(delete(SNote).where(SNote.id == snote_id))
        await self.db.commit()
