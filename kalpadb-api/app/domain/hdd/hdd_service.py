from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy import delete, func

from app.domain.hdd.hdd_model import HDD
from app.domain.hdd.hdd_schema import GroupItemResponse, HDDRequest, HDDResponse

class HDDService:
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def volumn_list(self) -> List[GroupItemResponse]:
        """HDD 그룹 리스트 조회"""
        query = (
            select(
                HDD.volumn_name.label("title"),
                func.count().label("count")
            )
            .where(HDD.gubun == 'D')
            .group_by(HDD.volumn_name)
        )

        # 비동기로 쿼리 실행
        results = await self.db.execute(query)
        rows = results.fetchall()
        # Pydantic 모델로 매핑 후 반환
        response_data = [
            GroupItemResponse(title=row.title, count=row.count) for row in rows
        ]

        return response_data        

    async def hdd_list(self, volumn_name: str, directory_only: bool) -> List[HDDResponse]:
        """ volumn_name에 해당하는 HDD 리스트 조회, directory_only=True일 경우 디렉토리만 조회 """
        query = select(HDD).where(HDD.volumn_name == volumn_name)
        if directory_only:
            query = query.where(HDD.gubun == 'D')

        # 비동기로 쿼리 실행
        results = await self.db.execute(query)
        rows = results.scalars().all()

        for row in rows:
            print(row)  # row의 구조를 확인합니다.
            print(type(row))  # 반환값의 타입을 확인합니다.
        
        # Pydantic 모델로 매핑 후 반환
        response_data = [HDDResponse.model_validate(row) for row in rows]

        return response_data
        
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
