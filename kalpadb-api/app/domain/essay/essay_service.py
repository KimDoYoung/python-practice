from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy import delete, func

from app.domain.essay.essay_model import Essay
from app.domain.essay.essay_schema import EssayListRequest, EssayListResponse, EssayRequest, EssayResponse, EssayUpsertRequest

class EssayService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_essay(self, essay_id: int) -> EssayResponse:
        """특정 ID로 에세이 조회"""
        result = await self.db.execute(select(Essay).where(Essay.id == essay_id))
        essay = result.scalar_one_or_none()
        if not essay:
            raise NoResultFound(f"Essay with ID {essay_id} not found")
        return EssayResponse.model_validate(essay)

    async def get_essays(self, request: EssayListRequest) -> EssayListResponse:
        """모든 에세이 조회 (최신 정렬)"""
        # GREATEST(create_dt, COALESCE(lastmodify_dt, create_dt))를 적용한 정렬 추가
        stmt = select(Essay)
        if request.search_text:
            stmt = stmt.where(Essay.title.contains(request.search_text) | Essay.content.contains(request.search_text))
        stmt = stmt.order_by(
            func.greatest(
                Essay.create_dt,
                func.coalesce(Essay.lastmodify_dt, Essay.create_dt)
            ).desc()
        )
        stmt = stmt.offset(request.start_index).limit(request.limit)
        
        # 쿼리 실행
        result = await self.db.execute(stmt)
        essays = result.scalars().all()
        # 현재 페이지 결과와 exists_next 판별
        exists_next = len(essays) > request.limit
        if exists_next:
            essays = essays[:-1]  # limit 초과분 제거        

        # ORM 모델을 Pydantic 응답 모델로 변환
        return EssayListResponse(
            essays=[EssayResponse.model_validate(essay) for essay in essays],
            exists_next=exists_next,
            last_index=request.start_index + len(essays) - 1,
            data_count=len(essays)
        )    

    async def upsert_essay(self, request: EssayUpsertRequest) -> EssayResponse:
        """에세이 생성 또는 수정"""
        if request.id:
            return await self.update_essay(request.id, EssayRequest(title=request.title, content=request.content))
        return await self.create_essay(EssayRequest(title=request.title, content=request.content))


    async def create_essay(self, essay_data: EssayRequest) -> EssayResponse:
        """에세이 생성"""
        essay = Essay(**essay_data.model_dump())
        self.db.add(essay)
        await self.db.commit()
        await self.db.refresh(essay)
        return EssayResponse.model_validate(essay)

    async def update_essay(self, essay_id: int, essay_data: EssayRequest) -> EssayResponse:
        """에세이 수정"""
        result = await self.db.execute(select(Essay).where(Essay.id == essay_id))
        essay = result.scalar_one_or_none()
        if not essay:
            raise NoResultFound(f"Essay with ID {essay_id} not found")
        
        for key, value in essay_data.model_dump(exclude_unset=True).items():
            setattr(essay, key, value)
        self.db.add(essay)
        await self.db.commit()
        await self.db.refresh(essay)
        return EssayResponse.model_validate(essay)

    async def delete_essay(self, essay_id: int) -> EssayResponse:
        """에세이 삭제"""
        result = await self.db.execute(select(Essay).where(Essay.id == essay_id))
        essay = result.scalar_one_or_none()
        if not essay:
            raise NoResultFound(f"Essay with ID {essay_id} not found")
        deleted_essay = EssayResponse.model_validate(essay)
        await self.db.execute(delete(Essay).where(Essay.id == essay_id))
        await self.db.commit()
        return deleted_essay
