from fastapi import APIRouter, Depends, HTTPException, Body, Path, Request
from fastapi.responses import JSONResponse
from backend.app.core.dependency import get_user_service
from backend.app.domains.stc.kis.kis_api import KoreaInvestmentApi
from backend.app.domains.user.user_model import User
from backend.app.domains.user.user_service import UserService

from backend.app.core.logger import get_logger
from backend.app.core.security import get_current_user

logger = get_logger(__name__)

# APIRouter 인스턴스 생성
router = APIRouter()

#TODO : 주식 잔고 조회
@router.get("/", response_class=JSONResponse)
async def info(request:Request, user_service :UserService=Depends(get_user_service)):
    current_user = await get_current_user(request)
    logger.debug(f"current_user : {current_user}")
    user_id = current_user.get('user_id')
    user = await user_service.get_user(user_id)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token-사용자 정보가 없습니다")
    
    kis_api = KoreaInvestmentApi(user)
    stk_code = "034020"
    cost = kis_api.get_current_price(stk_code)
    logger.debug(f"종목: {stk_code} : {cost}")
    balance = kis_api.get_balance()
    logger.debug(f"잔고 : {balance}")
    return {"message": "Hello, World!"}

