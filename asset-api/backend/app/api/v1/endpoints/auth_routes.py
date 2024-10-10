from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from backend.app.core.logger import get_logger
from backend.app.domain.auth.auth_schema import AuthRequest, AuthResponse
from backend.app.core.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.domain.company.company_service import get_company_by_app_key
from backend.app.core.security import create_access_token, secret_key_encrypt, verify_access_token

logger = get_logger(__name__)

router = APIRouter()

async def test_token(auth_resp, app_secret_key):
    ''' JWT 토큰 검증 '''
    try:
        logger.debug(f"Verifying token: {auth_resp.token} with secret: {app_secret_key}")
        payload = verify_access_token(auth_resp.token, app_secret_key)
        logger.debug(f"Token verified successfully: {payload}")
        
        if payload['company_id'] != auth_resp.company_id:
            return '토큰발급 테스트 - 올바르지 않은 토큰(회사ID)'
        if payload['service_id'] != auth_resp.service_id:
            return '토큰발급 테스트 - 올바르지 않은 토큰(서비스ID)'
        if payload['start_ymd'] != auth_resp.start_ymd:
            return '토큰발급 테스트 - 올바르지 않은 토큰(시작일)'
        if payload['end_ymd'] != auth_resp.end_ymd:
            return '토큰발급 테스트 - 올바르지 않은 토큰(종료일)'
        if datetime.now(timezone.utc).timestamp() > payload['exp']:
            return '토큰발급 테스트 - 만료된 토큰'
        return 'OK'
    except Exception as e:
        logger.error(f"Token verification failed: {str(e)}")
        return '토큰발급 테스트 - 올바르지 않은 토큰'

@router.post("/token",  response_model=AuthResponse)
async def auth(req: AuthRequest, db: AsyncSession = Depends(get_session)):
    ''' app key, secret key로 회사 정보 조회 후 token 발급, 토큰 검증 '''
    logger.debug(f"Auth request: APP_KEY: {req.app_key}\nAPP_SECRET_KEY: {req.app_secret_key}")
    company = await get_company_by_app_key(db, req.app_key)
    # 회사 정보가 없으면 404 에러
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    app_secret_key = req.app_secret_key
    data = f"{company.company_id}|{company.service_id}|{company.start_ymd}"
    
    app_secret_key_for_check = secret_key_encrypt(req.app_key, data)
    
    # request로 받은 app_secret_key가 일치하지 않으면 401 에러
    if app_secret_key != app_secret_key_for_check:
        raise HTTPException(status_code=401, detail="Unauthorized secret key is not correct")
    
    token = create_access_token(app_secret_key, company.company_id, company.service_id, company.start_ymd, company.end_ymd) 
    
    auth_resp = AuthResponse(
        company_id=company.company_id,
        service_id=company.service_id,
        start_ymd=company.start_ymd,
        end_ymd = company.end_ymd,
        token=token
    )
    # 발급한 토큰을 테스트해 봄
    check_msg = await test_token(auth_resp, app_secret_key)
    if check_msg != 'OK':
        raise HTTPException(status_code=403, detail=check_msg)
        
    logger.info("-------------------------------------------------")
    logger.info(f"JWT키 발급: Auth response: {auth_resp}")  
    logger.info("-------------------------------------------------")
    return auth_resp
    
    
    