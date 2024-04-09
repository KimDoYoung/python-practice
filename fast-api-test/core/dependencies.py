from contextlib import asynccontextmanager
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .database import AsyncSessionLocal
from service.item_service import ItemService
from typing import AsyncGenerator, Generator, Annotated
from sqlmodel import Session

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    db: AsyncSession = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()

def get_item_service() -> ItemService:
    return ItemService()

# db_dependency = Annotated[Session, Depends(get_db)]
# item_service_dependency = Annotated[Session, Depends(get_item_service)]

db_dependency = Annotated[AsyncSession, Depends(get_db)]
item_service_dependency = Annotated[ItemService, Depends(get_item_service)]