from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy import delete

from app.models.hdd_model import HDD
from app.schemas.hdd_schema import HDDRequest, HDDResponse

class HDDService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_hdd(self, hdd_id: int) -> HDDResponse:
        """특정 ID로 HDD 조회"""
        result = await self.db.execute(select(HDD).where(HDD.id == hdd_id))
        hdd = result.scalar_one_or_none()
        if not hdd:
            raise NoResultFound(f"HDD with ID {hdd_id} not found")
        return HDDResponse.from_orm(hdd)

    async def get_hdds(self) -> list[HDDResponse]:
        """모든 HDD 조회"""
        result = await self.db.execute(select(HDD))
        hdds = result.scalars().all()
        return [HDDResponse.from_orm(hdd) for hdd in hdds]

    async def create_hdd(self, hdd_data: HDDRequest) -> HDDResponse:
        """HDD 데이터 생성"""
        hdd = HDD(**hdd_data.dict())
        self.db.add(hdd)
        await self.db.commit()
        await self.db.refresh(hdd)
        return HDDResponse.from_orm(hdd)

    async def update_hdd(self, hdd_id: int, hdd_data: HDDRequest) -> HDDResponse:
        """HDD 데이터 수정"""
        result = await self.db.execute(select(HDD).where(HDD.id == hdd_id))
        hdd = result.scalar_one_or_none()
        if not hdd:
            raise NoResultFound(f"HDD with ID {hdd_id} not found")
        
        for key, value in hdd_data.dict(exclude_unset=True).items():
            setattr(hdd, key, value)
        self.db.add(hdd)
        await self.db.commit()
        await self.db.refresh(hdd)
        return HDDResponse.from_orm(hdd)

    async def delete_hdd(self, hdd_id: int) -> None:
        """HDD 데이터 삭제"""
        result = await self.db.execute(select(HDD).where(HDD.id == hdd_id))
        hdd = result.scalar_one_or_none()
        if not hdd:
            raise NoResultFound(f"HDD with ID {hdd_id} not found")
        
        await self.db.execute(delete(HDD).where(HDD.id == hdd_id))
        await self.db.commit()
