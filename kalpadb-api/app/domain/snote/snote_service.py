from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy import delete

from app.domain.snote.snote_model import SNote
from app.domain.snote.snote_schema import SNoteRequest, SNoteResponse, SnoteListRequest, SnoteListResponse

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

    async def get_snotes(self, req:SnoteListRequest ) -> list[SNoteResponse]:
        """모든 노트 조회"""
        # 검색 조건 설정
        search_text = req.search_text
        start_index = req.start_index
        limit = req.limit

        stmt = select(SNote)
        if search_text:
            stmt = stmt.where(SNote.title.like(f"%{search_text}%"))
        stmt = stmt.offset(start_index).limit(limit + 1)  # limit + 1로 조회하여 다음 페이지 여부 확인  

        # 실행
        result = await self.db.execute(stmt)
        rows = result.scalars().all()

        # 데이터 처리
        snote_list = [SNoteResponse.model_validate(row) for row in rows[:limit]]

        next_exist = len(rows) > limit  # 다음 페이지 데이터가 있는지 확인

        # 응답 생성
        response = SnoteListResponse(
            snote_list=snote_list,
            next_exist=next_exist,
            limit=limit,
            last_index=start_index + len(snote_list) - 1
        )

        return response

    async def upsert_snote(self, snote_id: int, snote_data: SNoteRequest) -> SNoteResponse:
        if snote_id:
            return await self.update_snote(snote_id, snote_data)
        else:
            return await self.create_snote(snote_data)

    async def update_snote(self, snote_id: int, snote_data: SNoteRequest) -> SNoteResponse:
        """노트 업데이트"""
        result = await self.db.execute(select(SNote).where(SNote.id == snote_id))
        snote = result.scalar_one_or_none()
        if not snote:
            raise NoResultFound(f"SNote with ID {snote_id} not found")
        
        snote.update(snote_data.model_dump())
        await self.db.commit()
        await self.db.refresh(snote)
        return SNoteResponse.model_validate(snote)
        
    async def create_snote(self, snote_data: SNoteRequest) -> SNoteResponse:
        """노트 생성"""
        snote = SNote(**snote_data.model_dump())
        self.db.add(snote)
        await self.db.commit()
        await self.db.refresh(snote)
        return SNoteResponse.model_validate(snote)

    async def delete_snote(self, snote_id: int) -> SNoteResponse:
        """노트 삭제"""
        result = await self.db.execute(select(SNote).where(SNote.id == snote_id))
        snote = result.scalar_one_or_none()
        if not snote:
            raise NoResultFound(f"SNote with ID {snote_id} not found")
        deleted_snote = SNoteResponse.model_validate(snote)
        
        await self.db.execute(delete(SNote).where(SNote.id == snote_id))
        await self.db.commit()
        return deleted_snote