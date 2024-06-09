from fastapi import APIRouter, Depends, HTTPException, Body, Path, Request
from fastapi.responses import JSONResponse
from backend.app.core.dependency import get_user_service
from backend.app.domains.stc.kis.kis_api import KoreaInvestmentApi
from backend.app.domains.user.user_model import User
from backend.app.domains.user.user_service import UserService

from backend.app.core.logger import get_logger
from backend.app.core.security import get_current_user
from backend.app.core.exception.kis_exception import KisAccessTokenExpireException, KisAccessTokenInvalidException

logger = get_logger(__name__)

# APIRouter 인스턴스 생성
router = APIRouter()

@router.get("/token", response_class=JSONResponse)
async def get_token_from_kis(request:Request, user_service :UserService=Depends(get_user_service)):
    '''
        1. 현재 사용자 DB에 있는 ACCESS_TOKEN으로 현재가를 조회하고  
        2. KIS_ACCESS_TOKEN_EXPIRE_EXCECPTION이 발생하면 
        3. 새로 token을 발급받아서 User DB에 저장한다.
    '''
    current_user = await get_current_user(request)
    logger.debug(f"current_user : {current_user}")
    user_id = current_user.get('user_id')
    user = await user_service.get_1(user_id)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token-사용자 정보가 없습니다")
    
    kis_api = KoreaInvestmentApi(user)
    
    try:
        cost = kis_api.get_current_price("005930") # 삼성전자
        logger.debug(f"삼성전자 현재가 : {cost}")
        return {"detail": "Access Token is valid."}
    except KisAccessTokenExpireException as e:
        logger.warning(f"현재 ACCESS_TOKEN은  만료되었습니다.")
        new_access_token=await kis_api.set_access_token_from_kis()
        logger.debug(f"새로운 ACCESS_TOKEN을 발급받음: [{new_access_token}]")
        return {"detail": "기존 Access Token이 만료되어 재발급받음. 이제 Access Token 은 유효함"}
    except KisAccessTokenInvalidException as e:
        logger.error(f"현재 ACCESS_TOKEN이 유효하지 않습니다.")
        new_access_token=await kis_api.set_access_token_from_kis()
        return {"detail": "기존 Access Token이 유효하지 않아 재발급받음. 이제 Access Token 은 유효함"}
    

#TODO : 주식 잔고 조회
@router.get("/", response_class=JSONResponse)
async def info(request:Request, user_service :UserService=Depends(get_user_service)):
    current_user = await get_current_user(request)
    logger.debug(f"current_user : {current_user}")
    user_id = current_user.get('user_id')
    user = await user_service.get_1(user_id)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token-사용자 정보가 없습니다")
    
    kis_api = KoreaInvestmentApi(user)
    stk_code = "034020"
    cost = kis_api.get_current_price(stk_code)
    logger.debug(f"종목: {stk_code} : {cost}")
    balance = kis_api.get_balance()
    logger.debug(f"잔고 : {balance}")
    return {"message": "Hello, World!"}

