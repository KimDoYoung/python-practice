from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, func

from app.domain.hdd.hdd_model import HDD
from app.domain.hdd.hdd_schema import GroupItemResponse, HDDChildRequest, HDDResponse, HDDSearchRequest, HDDSearchResponse

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

    async def hdd_child_list(self, childreq: HDDChildRequest) -> List[HDDResponse]:
        """ volumn_name, pid, gubun에 해당하는 HDD 리스트 조회 """
        
        query = select(HDD).where(HDD.volumn_name == childreq.volumn_name)

        if childreq.pid == 0:
            query = query.where(HDD.pid == None)
        else:
            query = query.where(HDD.pid == childreq.pid)

        if childreq.gubun != 'A':
            query = query.where(HDD.gubun == childreq.gubun)

        # 비동기로 쿼리 실행
        results = await self.db.execute(query)
        rows = results.scalars().all()
        
        # Pydantic 모델로 매핑 후 반환
        response_data = [HDDResponse.model_validate(row) for row in rows]
        return response_data

    async def search_hdd(self, request: HDDSearchRequest) -> HDDSearchResponse:
        """
        HDD 테이블에서 조건에 따라 데이터를 조회하고 응답 객체를 반환합니다.

        Args:
            request (HDDSearchRequest): 검색 조건을 포함한 요청 객체

        Returns:
            HDDSearchResponse: 조회된 결과 및 메타데이터를 포함한 응답 객체
        """
        # 동적 where 조건 생성
        conditions = []
        if request.search_text:
            conditions.append(func.concat(HDD.path, HDD.name).like(f"%{request.search_text}%"))
        if request.gubun and request.gubun != 'A':  # 'A'는 조건에서 제외
            conditions.append(HDD.gubun == request.gubun)

        # SQLAlchemy 쿼리 작성
        query = (
            select(HDD)
            .where(and_(*conditions))
            .order_by(HDD.volumn_name, HDD.path)
            .offset(request.start_index)
            .limit(request.limit + 1)  # limit + 1로 추가 데이터 여부 확인
        )

        # 쿼리 실행
        result = await self.db.execute(query)
        rows = result.scalars().all()

        # 데이터 변환
        data = [HDDResponse.model_validate(row) for row in rows[: request.limit]]  # 실제 데이터 제한
        next_data_exists = len(rows) > request.limit  # 추가 데이터 존재 여부 확인

        # 응답 객체 생성
        return HDDSearchResponse(
            list=data,
            data_count=len(data),
            next_data_exists=next_data_exists,
            last_index=request.start_index + len(data),
            limit=request.limit,
        )