# backend/app/core/constants.py
# constants.py
from dotenv import load_dotenv
import os

# 환경 변수나 어플리케이션의 설정을 통해 현재 환경을 결정
MERIAN_PROFILE = os.getenv('MERIAN_MODE', 'local')
env_path = f'.env.{MERIAN_PROFILE}'
load_dotenv(dotenv_path=env_path)

# 환경변수를 읽어와서 상수에 할당합니다.
MERIAN_PORT=int(os.getenv('PORT', 8686))

DATABASE_URL = os.getenv("DB_URL")


if MERIAN_PROFILE == "local":
    LOG_FILE = "c:\\tmp\\logs\\merian\\merian.log"
    FILE_DIR="c:\\tmp\\files\\merian"
else:  
    LOG_FILE="/logs/merian/merian.log"
    FILE_DIR="/filees/merian"

LOG_DIR = os.path.dirname(LOG_FILE)  

# 해당 디렉터리가 없으면 생성
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR, exist_ok=True) 

    
# JWT를 위한 비밀키와 알고리즘 설정
SECRET_KEY = "a_very_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
