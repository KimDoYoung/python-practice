from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

from jangbi_model import Jangbi
from jangbi_schema import JangbiRequest

class JangbiService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def upsert_jangbi(self, jangbi_id: Optional[int], request: JangbiRequest) -> Jangbi:
        """
        데이터가 존재하면 업데이트, 존재하지 않으면 새로 삽입한다.
        
        :param jangbi_id: 업데이트할 대상 ID (없으면 새로 생성)
        :param request: JangbiRequest 데이터
        :return: 생성되거나 업데이트된 Jangbi 객체
        """
        if jangbi_id:
            # 기존 데이터 확인
            existing_jangbi = await self.get_jangbi_by_id(jangbi_id)
            if existing_jangbi:
                # 업데이트 수행
                existing_jangbi.ymd = request.ymd
                existing_jangbi.item = request.item
                existing_jangbi.location = request.location
                existing_jangbi.cost = request.cost
                existing_jangbi.spec = request.spec
                existing_jangbi.lvl = request.lvl

                await self.db.commit()
                await self.db.refresh(existing_jangbi)
                return existing_jangbi

        # 존재하지 않으면 새로 생성
        new_jangbi = Jangbi(
            ymd=request.ymd,
            item=request.item,
            location=request.location,
            cost=request.cost,
            spec=request.spec,
            lvl=request.lvl
        )
        self.db.add(new_jangbi)
        await self.db.commit()
        await self.db.refresh(new_jangbi)
        return new_jangbi


    async def get_jangbi_by_id(self, jangbi_id: int) -> Optional[Jangbi]:
        query = select(Jangbi).where(Jangbi.id == jangbi_id)
        result = await self.db.execute(query)
        jangbi = result.scalar_one_or_none()
        return jangbi

    async def list_jangbis(self) -> List[Jangbi]:
        query = select(Jangbi)
        result = await self.db.execute(query)
        return result.scalars().all()


    async def delete_jangbi(self, jangbi_id: int) -> bool:
        jangbi = await self.get_jangbi_by_id(jangbi_id)
        if not jangbi:
            return False

        await self.db.delete(jangbi)
        await self.db.commit()
        return True
