import jwt
import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
import hashlib

# AES 암호화 함수 (app_secret_key 생성용)
def aes_encrypt(key:str, data:str) -> str:
    '''AES 암호화 함수'''
    key = hashlib.sha256(key.encode('utf-8')).digest()[:32]
    cipher = AES.new(key, AES.MODE_ECB)
    padded_data = pad(data.encode('utf-8'), AES.block_size)
    encrypted = cipher.encrypt(padded_data)
    return base64.b64encode(encrypted).decode('utf-8')

# JWT 토큰 생성 함수 (app_secret_key를 SECRET_KEY로 사용)
def generate_jwt(company_id, service_id, app_secret_key):
    """JWT 토큰을 발급하는 함수"""
    
    # 현재 시간
    current_time = datetime.datetime.now(datetime.timezone.utc)
    
    # 만료 시간 (24시간 후)
    expiration_time = current_time + datetime.timedelta(hours=24)
    
    # JWT에 담을 클레임 (payload)
    payload = {
        'company_id': company_id,           # 회사 ID
        'service_id': service_id,           # 서비스 ID
        'iat': current_time,                # 발급 시간 (issued at)
        'exp': expiration_time              # 만료 시간 (expiration)
    }
    
    # JWT 토큰 생성 (app_secret_key를 사용하여 서명)
    token = jwt.encode(payload, app_secret_key, algorithm='HS256')
    
    return token

# JWT 토큰 검증 함수 (app_secret_key로 서명 검증)
def verify_jwt(token, app_secret_key):
    """JWT 토큰을 검증하는 함수"""
    
    try:
        # 토큰을 디코드 (검증)하고, 유효하다면 payload 반환
        payload = jwt.decode(token, app_secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return "토큰이 만료되었습니다."
    except jwt.InvalidTokenError:
        return "유효하지 않은 토큰입니다."

# 회사 정보
company_id = 12345
service_id = "법률서비스"
start_date = "20231001"

# 1. app_secret_key 생성 (AES 암호화)
aes_key = "kfs-restful-zaq1@WSX"  # 고정 AES 키
data_to_encrypt = f"{company_id}|{service_id}|{start_date}"
app_secret_key = aes_encrypt(aes_key, data_to_encrypt)

# 2. JWT 토큰 발급 (app_secret_key를 SECRET_KEY로 사용)
token = generate_jwt(company_id, service_id, app_secret_key)
print("발급된 JWT 토큰:", token)

# 3. JWT 토큰 검증 (app_secret_key로 검증)
result = verify_jwt(token, app_secret_key)
print("JWT 검증 결과:", result)
