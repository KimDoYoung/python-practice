from fastapi import HTTPException
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
