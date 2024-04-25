from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from fastapi import HTTPException

from backend.app.domains.user.appkey_model import AppKey, AppKeyBase
from backend.app.core.exceptions.joanna_exceptions import JoannaException

class AppKeyService:
    async def insert(self, app_key: AppKey, session: AsyncSession) -> AppKey:
        '''
        앱 키를 등록한다.
        이미 존재하는 앱 키라면 409 에러를 발생시킨다.
        등록 후 조회하여 반환한다.
        '''
        statement = select(AppKey).filter(and_(AppKey.user_id == app_key.user_id, AppKey.key_name == app_key.key_name))
        result = await session.execute(statement)
        if result.scalars().first() is not None:
            raise JoannaException(status_code=409, detail=f"App key {app_key.user_id}-{app_key.key_name} already exists.")
        session.add(app_key)
        await session.commit()
        app_key_base = AppKeyBase(user_id=app_key.user_id, key_name=app_key.key_name)
        return await self.get(app_key_base, session)

    async def get(self, app_key: AppKeyBase, session: AsyncSession) -> AppKey:
        '''
        앱 키를 조회한다.
        '''
        statement = select(AppKey).filter(and_(AppKey.user_id == app_key.user_id, AppKey.key_name == app_key.key_name))
        result = await session.execute(statement)
        if result is None:
            raise JoannaException(status_code=404, detail=f"App key {app_key.user_id}-{app_key.key_name} not found.")
        return result.scalars().first()

    async def delete(self,app_key: AppKeyBase, session: AsyncSession) -> None:
        '''
        앱 키를 삭제한다.
        '''
        statement = select(AppKey).filter(and_(AppKey.user_id == app_key.user_id, AppKey.key_name == app_key.key_name))
        result = await session.execute(statement)
        app_key = result.scalars().first()
        if app_key is None:
            raise JoannaException(status_code=404, detail=f"App key {app_key.user_id}-{app_key.key_name} not found.")
        await session.delete(app_key)
        await session.commit()
        return None

    async def update(self, app_key: AppKey, session: AsyncSession) -> AppKey:
        '''
        앱 키를 수정한다.
        수정 후 조회하여 반환한다.
        '''
        statement = select(AppKey).where(AppKey.user_id == app_key.user_id and AppKey.key_name == app_key.key_name)
        result = await session.execute(statement)
        existing_app_key = result.scalars().first()
        if existing_app_key is None:
            raise JoannaException(status_code=404, detail=f"App key {app_key.user_id}-{app_key.key_name} not found.")
        existing_app_key.key = app_key.key
        await session.commit()
        return await self.get(app_key.id, session)

    async def get_all(self, session: AsyncSession) -> List[AppKey]:
        '''
        모든 키를 조회한다.
        '''
        statement = select(AppKey).order_by(AppKey.created_at.desc())
        result = await session.execute(statement)
        return result.scalars().all()