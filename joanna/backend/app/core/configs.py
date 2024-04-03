# config.py
from dotenv import load_dotenv
import os

# 현재 환경에 맞는 .env 파일을 로드하는 함수
def load_environment(env_mode):
    dotenv_path = f'.env.{env_mode}'
    load_dotenv(dotenv_path=dotenv_path)

# 환경 변수를 통해 현재 모드를 결정
env_mode = os.getenv('JOANNA_MODE', 'production')
load_environment(env_mode)

# 데이터베이스
DATABASE_URI = os.getenv('DATABASE_URI')

# 한국투자증권 API
KOREA_INVESTMENT_APP_KEY = os.getenv('KOREA_INVESTMENT_APP_KEY')
KOREA_INVESTMENT_APP_SECRET = os.getenv('KOREA_INVESTMENT_APP_SECRET')
KOREA_INVESTMENT_URL_BASE = os.getenv('KOREA_INVESTMENT_URL_BASE')

if env_mode == "local":
    LOG_FILE = "c:\\tmp\\logs\\joanna\\joanna.log"
    FILE_DIR="c:\\tmp\\files\\joanna"
else:  
    LOG_FILE="/logs/joanna/joanna.log"
    FILE_DIR="/files/joanna"