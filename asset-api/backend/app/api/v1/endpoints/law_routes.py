from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.logger import get_logger
from backend.app.core.database import get_session
logger = get_logger(__name__)

router = APIRouter()

@router.get("/law/r010",  response_model=List[dict])
async def r010(db: AsyncSession = Depends(get_session)):
    # 1. 91에서 layout_cd -> LAW010 찾음.
    # 2. 92에서 LAW010으로 
    pass
