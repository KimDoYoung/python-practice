from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from backend.app.core.logger import get_logger
from backend.app.domain.auth.auth_schema import AuthPayload, AuthRequest, AuthResponse, Authtoken
from backend.app.core.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.domain.ifi.ifi01.ifi01_company_api_service import Ifi01CompanyApiService
from backend.app.core.security import create_access_token, secret_key_encrypt, verify_access_token

logger = get_logger()

router = APIRouter()

async def test_token(auth_resp):
    ''' JWT 토큰 검증 '''
    try:
        logger.debug(f"Verifying token: {auth_resp.token}")
        payload = verify_access_token(auth_resp.token)
        logger.debug(f"Token verified successfully: {payload}")

        if payload['company_api_id'] != auth_resp.company_api_id:
            return '토큰발급 테스트 - 올바르지 않은 토큰(회사ID)'
        if payload['company_id'] != auth_resp.company_id:
            return '토큰발급 테스트 - 올바르지 않은 토큰(회사ID)'
        if payload['service_cd'] != auth_resp.service_cd:
            return '토큰발급 테스트 - 올바르지 않은 토큰(서비스ID)'
        if payload['start_date'] != auth_resp.start_date:
            return '토큰발급 테스트 - 올바르지 않은 토큰(시작일)'
        if payload['close_date'] != auth_resp.close_date:
            return '토큰발급 테스트 - 올바르지 않은 토큰(종료일)'
        if datetime.now(timezone.utc).timestamp() > payload['exp']:
            return '토큰발급 테스트 - 만료된 토큰'
        return 'OK'
    except Exception as e:
        logger.error(f"Token verification failed: {str(e)}")
        return '토큰발급 테스트 - 올바르지 않은 토큰'

@router.post("/token",  response_model=AuthResponse)
async def generate_token(req: AuthRequest, db: AsyncSession = Depends(get_session)):
    ''' app key, secret key로 회사 정보 조회 후 token 발급, 토큰 검증 '''
    logger.debug(f"Auth request: APP_KEY: {req.app_key}\nAPP_SECRET_KEY: {req.app_secret_key}")
    company = await Ifi01CompanyApiService.get_company_by_app_key(req.app_key)
    # 회사 정보가 없으면 404 에러
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    app_secret_key = req.app_secret_key
    data = f"{company.ifi01_company_id}|{company.ifi01_service_cd}|{company.ifi01_start_date}"
    
    app_secret_key_for_check = secret_key_encrypt(req.app_key, data)
    
    # request로 받은 app_secret_key가 일치하지 않으면 401 에러
    if app_secret_key != app_secret_key_for_check:
        raise HTTPException(status_code=401, detail="Unauthorized secret key is not correct")
    
    token = create_access_token(company.ifi01_company_api_id, company.ifi01_company_id, company.ifi01_service_cd, str(company.ifi01_start_date), str(company.ifi01_close_date)) 
    
    auth_resp = AuthResponse(
        company_api_id=str(company.ifi01_company_api_id),
        company_id=str(company.ifi01_company_id),
        service_cd=str(company.ifi01_service_cd),
        start_date=str(company.ifi01_start_date).replace('-', ''),
        close_date = str(company.ifi01_close_date).replace('-', ''),
        token=token
    )
    # 발급한 토큰을 테스트해 봄
    check_msg = await test_token(auth_resp)
    if check_msg != 'OK':
        raise HTTPException(status_code=403, detail=check_msg)
        
    logger.info("-------------------------------------------------")
    logger.info(f"JWT키 발급: Auth response: {auth_resp}")  
    logger.info("-------------------------------------------------")
    return auth_resp
    

@router.post("/token/verify",  response_model=AuthPayload)
async def verify(authToken: Authtoken, db: AsyncSession = Depends(get_session)):    
    ''' app key, secret key로 회사 정보 조회 후 token 발급, 토큰 검증 ''' 
    payload = verify_access_token(authToken.token)
    authpayload = AuthPayload(
        company_api_id = payload['company_api_id'],
        company_id=payload['company_id'],
        service_cd=payload['service_cd'],
        start_date=payload['start_date'],
        close_date=payload['close_date'],
        exp=payload['exp']
    )
    return authpayload