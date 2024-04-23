from typing import List
from fastapi import HTTPException
from sqlalchemy import and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select  
from backend.app.domains.openapi.dart_model import DartCorpCode


class DartService:
    async def get_corp_code(self, session: AsyncSession, corp_code: str) -> DartCorpCode:
        ''' 기업 코드로 기업 정보를 조회한다.'''
        statement = select(DartCorpCode).where(DartCorpCode.corp_code == corp_code)
        result = await session.execute(statement)
        if result is None:
            raise HTTPException(status_code=404, detail=f"Corp code {corp_code} not found.")
        return result.scalars().first()
        
    async def insert_corp_code(self, dcc: DartCorpCode, session: AsyncSession) -> DartCorpCode:
        ''' 
            기업 코드를 등록한다. 
            이미 존재하는 기업 코드라면 409 에러를 발생시킨다.
            Insert 후 조회하여 반환한다.
        '''
        statement = select(DartCorpCode).where(DartCorpCode.corp_code == dcc.corp_code)
        result = await session.execute(statement)
        if result.scalars().first() is not None:
            raise HTTPException(status_code=409, detail=f"Corp code {dcc.corp_code} already exists.")
        session.add(dcc)
        await session.commit()
        return await self.get_corp_code(session, dcc.corp_code)

    async def get_all(self, session: AsyncSession, 
                    searchText: str, skip: int, limit: int) -> List[DartCorpCode]:
        ''' 기업명 or stock_code로 기업 정보를 조회한다. searchText가 비어있으면 모든 기업 정보 조회.
            또한, 모든 조회에서 stock_code는 null이 아니어야 한다.
        '''

        # stock_code가 null이 아닌 조건을 항상 포함
        conditions = [DartCorpCode.stock_code.isnot(None)]

        if searchText:
            # searchText가 비어있지 않은 경우 검색 조건을 추가
            search_condition = or_(
                DartCorpCode.corp_name.like(f"%{searchText}%"),
                DartCorpCode.corp_code.like(f"%{searchText}%")
            )
            conditions.append(search_condition)

        # 모든 조건을 and_로 묶어 where 절에 적용
        statement = select(DartCorpCode).where(and_(*conditions)).offset(skip).limit(limit)

        result = await session.execute(statement)
        return result.scalars().all()