from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select  
from backend.app.domains.openapi.dart_model import DartCorpCode
from backend.app.domains.user.user_model import User


class UserService:
    async def get(self, session: AsyncSession, user_id: str) -> User:
        ''' 사용자 정보를 조회한다.'''
        statement = select(User).where(User.user_id == user_id)
        result = await session.execute(statement)
        if result is None:
            raise HTTPException(status_code=404, detail=f"User {user_id} not found.")
        return result.scalars().first()
        
    async def insert(self, user: User, session: AsyncSession) -> User:
        ''' 
            '''
        statement = select(User).where(User.user_id == user.user_id)
        result = await session.execute(statement)
        if result.scalars().first() is not None:
            raise HTTPException(status_code=409, detail=f"User {user.user_id} already exists.")
        session.add(user)
        await session.commit()
        return await self.get(session,user.user_id)
    
