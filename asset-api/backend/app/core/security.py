# security.py
"""
모듈 설명: 
    - 보안 관련 모듈
주요 기능:
    - aes_encrypt : AES 암호화 함수, app_secret_key 생성용
    - create_access_token : JWT 토큰 생성
    - verify_access_token : JWT 토큰 검증
    - get_current_company : 현재 회사 정보 반환

작성자: 김도영
작성일: 2024-10-04
버전: 1.0
"""
import base64
from datetime import datetime, timedelta
import hashlib
from fastapi import HTTPException, Request
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from jose import JWTError, jwt
from typing import Optional
from backend.app.core.settings import config
from fastapi import status

from backend.app.domain.company.company_service import get_company
from database import get_session


# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# def get_password_hash(password):
#     return pwd_context.hash(password)


def aes_encrypt( data:str) -> str:
    '''AES 암호화 함수, app_secret_key 생성용'''
    global_key = config.AES_GLOBAL_KEY
    key = hashlib.sha256(global_key.encode('utf-8')).digest()[:32]
    cipher = AES.new(key, AES.MODE_ECB)
    padded_data = pad(data.encode('utf-8'), AES.block_size)
    encrypted = cipher.encrypt(padded_data)
    return base64.b64encode(encrypted).decode('utf-8')

def create_access_token(app_secret_key:str, company_id: int, service_id: str, start_date: str):
    """
    JWT 토큰 생성
    :param data: 토큰에 포함할 추가 데이터 (예: 사용자 정보 등)
    :param company_id: 회사 ID
    :param service_id: 서비스 ID
    :param start_date: 서비스 시작 날짜
    :param expires_delta: 토큰 만료 시간 (기본값은 설정 파일에서 가져옴)
    :return: 생성된 JWT 토큰
    """
    ACCESS_TOKEN_EXPIRE_HOURS = config.ACCESS_TOKEN_EXPIRE_HOURS
    
    # 만료 시간 설정
    current_time = datetime.datetime.now(datetime.timezone.utc)
    expire = current_time + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    # JWT에 담을 클레임 (payload)
    payload = {
        "company_id": company_id,
        "service_id": service_id,
        "start_date": start_date,
        "exp": expire
    }

    token = jwt.encode(payload, app_secret_key, algorithms=['HS256'])  # JWT 생성
    
    return token


def verify_access_token(token: str, app_secret_key: str):
    '''JWT 토큰을 검증, payload 반환'''
    try:
        payload = jwt.decode(token, app_secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# JWT 토큰을 받기 위한 OAuth2PasswordBearer 설정
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl=ACCESS_TOKEN_NAME)
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


async def get_current_company(request: Request) -> dict:
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Authorization 헤더에서 토큰 추출
    token: Optional[str] = None
    authorization: str = request.headers.get("Authorization")
    if authorization and authorization.startswith("Bearer "):
        token = authorization[len("Bearer "):]

    if token is None:
        raise credentials_exception

    try:
        payload = verify_access_token(token)
        info: str = payload.get("service_info")
        if info is None:
            raise credentials_exception
        #{company_id}|{service_id}|{start_date}
        company_id, service_id, start_date = info.split("|")
        
    except JWTError:
        raise credentials_exception

    current_company = await get_company(get_session(),company_id,service_id)
    if current_company is None:
        raise credentials_exception
    
    company_dict = current_company.to_dict()

    return company_dict