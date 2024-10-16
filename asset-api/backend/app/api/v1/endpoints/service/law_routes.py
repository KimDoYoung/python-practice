from typing import Any, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.logger import get_logger
from backend.app.core.database import get_session
from backend.app.domain.service.law.law_schema import Law010_Request
from backend.app.domain.service.law.law_service import LawService
logger = get_logger(__name__)

router = APIRouter()

@router.get("/r010",  response_model=List[dict[str, Any]])
async def r010(
    conti_limit: int = Query(10, ge=1, le=1000, description="연속 조회 LIMIT"),
    conti_start_idx: int = Query(0, ge=0, description="연속 조회 START INDEX"),
    conti_yn: str = Query("N", description="연속 조회 여부 (Y/N)"),
    db: AsyncSession = Depends(get_session)
):
    service = LawService(db)
    req = Law010_Request(conti_limit=conti_limit, conti_start_idx=conti_start_idx, conti_yn=conti_yn)
    resp = service.run_r010(req)
    logger.info("======================================")
    logger.info(f"resp: {resp}")
    logger.info("======================================")
    return resp.dict()