import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

def get_aes_key_from_string(key_str, key_size=32):
    """긴 키 문자열을 AES에서 사용 가능한 고정 길이의 키로 변환"""
    hashed_key = hashlib.sha256(key_str.encode('utf-8')).digest()  # SHA-256으로 해시하여 32바이트 키 생성
    return hashed_key[:key_size]  # AES에서 요구하는 크기로 자름 (32바이트 사용)

def aes_encrypt(key, data):
    cipher = AES.new(key, AES.MODE_ECB)
    padded_data = pad(data.encode('utf-8'), AES.block_size)
    encrypted = cipher.encrypt(padded_data)
    return base64.b64encode(encrypted).decode('utf-8')

def aes_decrypt(key, encrypted_data):
    cipher = AES.new(key, AES.MODE_ECB)
    decoded_encrypted_data = base64.b64decode(encrypted_data)
    decrypted = unpad(cipher.decrypt(decoded_encrypted_data), AES.block_size)
    return decrypted.decode('utf-8')

# 긴 키 문자열
long_key = "this_is_a_very_long_secret_key_that_exceeds_the_aes_key_size_limit"

# 긴 문자열을 AES 32바이트 키로 변환
aes_key = get_aes_key_from_string(long_key)

# 암호화할 데이터
data = "A회사|법률서비스|20231001"

# AES 암호화
app_key = aes_encrypt(aes_key, data)
print("암호화된 App Key:", app_key)

# AES 복호화 (확인용)
decrypted_data = aes_decrypt(aes_key, app_key)
print("복호화된 데이터:", decrypted_data)
