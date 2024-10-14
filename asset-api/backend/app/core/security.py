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
import base64, hashlib
from datetime import datetime, timedelta, timezone
import random
import string
from fastapi import HTTPException, Request, status
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from jose import ExpiredSignatureError, JWTError, jwt
from typing import Optional

from backend.app.core.settings import config
from backend.app.utils.misc_util import toYmd

def generate_app_key(length: int = 64) -> str:
    """랜덤으로 영문 대소문자와 숫자를 조합한 app_key 생성"""
    characters = string.ascii_letters + string.digits  # 영문 대소문자 + 숫자
    app_key = ''.join(random.choice(characters) for _ in range(length))  # length만큼 랜덤 생성
    return app_key

def secret_key_encrypt(key:str, data:str) -> str:
    '''AES 암호화 함수, app_secret_key 생성용'''
    global_key = key
    key = hashlib.sha256(global_key.encode('utf-8')).digest()[:32]
    cipher = AES.new(key, AES.MODE_ECB)
    padded_data = pad(data.encode('utf-8'), AES.block_size)
    encrypted = cipher.encrypt(padded_data)
    return base64.b64encode(encrypted).decode('utf-8')

def secret_key_decrypt(key, encrypted_data):
    """AES 복호화 함수 (ECB 모드)"""
    global_key = key
    cipher = AES.new(global_key, AES.MODE_ECB)
    decoded_encrypted_data = base64.b64decode(encrypted_data)  # base64 디코딩
    decrypted = unpad(cipher.decrypt(decoded_encrypted_data), AES.block_size)  # 복호화 후 패딩 제거
    return decrypted.decode('utf-8')


def create_access_token(company_api_id: int, company_id: int, config_api_id: int, start_date: datetime, end_date: datetime) -> str:
    """
    JWT 토큰 생성
    :param data: 토큰에 포함할 추가 데이터 (예: 사용자 정보 등)
    :param company_id: 회사 ID
    :param service_id: 서비스 ID
    :param start_date: 서비스 시작 날짜
    :param expires_delta: 토큰 만료 시간 (기본값은 설정 파일에서 가져옴)
    :return: 생성된 JWT 토큰
    """
    ACCESS_TOKEN_EXPIRE_HOURS = int(config.ACCESS_TOKEN_EXPIRE_HOURS)
    # 만료 시간 설정
    current_time = datetime.now(timezone.utc)
    expire = current_time + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    # JWT에 담을 클레임 (payload)
    payload = {
        "company_api_id": company_api_id,
        "company_id": company_id,
        "config_api_id": config_api_id,
        "start_ymd": toYmd(start_date),
        "end_ymd" : toYmd(end_date),
        "exp": expire
    }
    # app_secret_key를 시크릿 키로 사용하여 JWT 생성
    jwt_secret_key = config.JWT_SECRET_KEY
    token = jwt.encode(payload, jwt_secret_key, algorithm='HS256')
    
    return token


def verify_access_token(token: str):
    '''JWT 토큰을 검증, payload 반환'''
    try:
        jwt_secret_key = config.JWT_SECRET_KEY
        payload = jwt.decode(token, jwt_secret_key, algorithms=['HS256'])

        if not is_date_valid(payload['start_ymd'], payload['end_ymd']):
            raise HTTPException(status_code=401, detail="Invalid date, service date over")
        
        return payload
    # 서명이 만료된 경우
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    
    # JWT 관련 오류는 모두 JWTError로 처리
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
def is_date_valid(start_ymd: str, end_ymd: str):
    '''날짜 유효성 검증, 오늘이 시작일과 종료일 사이에 있는지 확인'''
    current_time = datetime.now(timezone.utc)
    # 입력받은 날짜를 UTC의 aware datetime 객체로 변환
    start_time = datetime.strptime(start_ymd, '%Y%m%d').replace(tzinfo=timezone.utc)
    end_time = datetime.strptime(end_ymd, '%Y%m%d').replace(tzinfo=timezone.utc)
    if current_time < start_time or current_time > end_time:
        return False
    return True

# async def company_exist_check(company_id: int, service_id: str):
#     '''회사 정보 존재 여부 확인'''
#     company = await get_company(company_id, service_id)
#     if company is None:
#         return False
#     return True        

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
    company_dict = {}
    try:
        payload = verify_access_token(token)
        info: str = payload.get("service_info")
        if info is None:
            raise credentials_exception
        #{company_id}|{service_id}|{start_date}
        company_api_id,company_id,config_api_id,start_date,end_date,exp   = info.split("|")
        company_dict = {
            "company_api_id": company_api_id,
            "company_id": company_id,
            "config_api_id": config_api_id,
            "start_ymd": start_date,
            "end_ymd": end_date,
            "exp": exp
        }

    except JWTError:
        raise credentials_exception

    return company_dict