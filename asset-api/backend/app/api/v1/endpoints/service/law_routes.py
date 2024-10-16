from typing import Any, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.logger import get_logger
from backend.app.core.database import get_session
logger = get_logger(__name__)

router = APIRouter()

@router.get("/r010",  response_model=List[dict[str, Any]])
async def r010(
    conti_limit: int = Query(10, ge=1, le=1000, description="연속 조회 LIMIT"),
    conti_start_idx: int = Query(0, ge=0, description="연속 조회 START INDEX"),
    conti_yn: str = Query("N", description="연속 조회 여부 (Y/N)"),
    db: AsyncSession = Depends(get_session)
):
    # 1. 91에서 layout_cd -> LAW010 찾음.
    # 2. 92에서 LAW010으로 
    dict_list = []
    dict_list.append({"layout_cd": "LAW010", "layout_nm": "법령조문"})
    dict_list.append({"layout_cd": "LAW010", "layout_nm": "법령조문"})
    dict_list.append({"layout_cd": "LAW010", "layout_nm": "법령조문"})
    return dict_list