import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

# 긴 AES 키 문자열을 32바이트로 변환
def get_aes_key_from_long_string(long_key):
    """긴 AES 키를 SHA-256을 통해 32바이트로 압축"""
    return hashlib.sha256(long_key.encode('utf-8')).digest()  # 32바이트(256비트) AES 키 생성

# AES 암호화 함수
def aes_encrypt(key, data):
    """AES 암호화 함수 (ECB 모드)"""
    cipher = AES.new(key, AES.MODE_ECB)  # AES 암호화 객체 생성 (ECB 모드 사용)
    padded_data = pad(data.encode('utf-8'), AES.block_size)  # 데이터를 블록 크기로 패딩
    encrypted = cipher.encrypt(padded_data)  # 암호화
    return base64.b64encode(encrypted).decode('utf-8')  # base64 인코딩 후 반환

# AES 복호화 함수 (확인용)
def aes_decrypt(key, encrypted_data):
    """AES 복호화 함수 (ECB 모드)"""
    cipher = AES.new(key, AES.MODE_ECB)
    decoded_encrypted_data = base64.b64decode(encrypted_data)  # base64 디코딩
    decrypted = unpad(cipher.decrypt(decoded_encrypted_data), AES.block_size)  # 복호화 후 패딩 제거
    return decrypted.decode('utf-8')

# 매우 긴 AES 키 문자열
long_aes_key = "한국펀드서비스-RestfulAPI-Service-202410-ZAQ!2wsx"

# 긴 키 문자열을 32바이트로 변환
aes_key = get_aes_key_from_long_string(long_aes_key)
print("APP 키:", aes_key)
# 암호화할 데이터 (회사명, 서비스명, 시작일)
company_id = "A회사"
service_id = "법률서비스"
start_date = "20231001"
data_to_encrypt = f"{company_id}|{service_id}|{start_date}"

# AES 암호화
app_secret = aes_encrypt(aes_key, data_to_encrypt)

# 결과 출력
print("암호화된 App Secret:", app_secret)

# 복호화 (확인용)
decrypted_data = aes_decrypt(aes_key, app_secret)
print("복호화된 데이터:", decrypted_data)
