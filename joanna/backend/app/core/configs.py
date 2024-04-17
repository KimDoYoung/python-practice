# config.py
from dotenv import load_dotenv
import os

# 현재 환경에 맞는 .env 파일을 로드하는 함수
def load_environment(env_mode):
    dotenv_path = f'.env.{env_mode}'
    load_dotenv(dotenv_path=dotenv_path)

# 환경 변수를 통해 현재 모드를 결정
env_mode = os.getenv('JOANNA_MODE', 'local')
print("=====================================  env_mode  =====================================")
print(f"env_mode: {env_mode}")
print("=====================================  env_mode  =====================================")
load_environment(env_mode)

# 데이터베이스
DATABASE_URI = os.getenv('DATABASE_URI')

# 한국투자증권 API
KOREA_INVESTMENT_APP_KEY = os.getenv('KOREA_INVESTMENT_APP_KEY')
KOREA_INVESTMENT_APP_SECRET = os.getenv('KOREA_INVESTMENT_APP_SECRET')
KOREA_INVESTMENT_URL_BASE = os.getenv('KOREA_INVESTMENT_URL_BASE')

DATA_GO_KR_API_KEY = os.getenv('DATA_GO_KR_API_KEY')

if env_mode == "local":
    LOG_FILE = "c:\\tmp\\logs\\joanna\\joanna.log"
else:  
    LOG_FILE="/logs/joanna/joanna.log"

# 로그파일폴더가 존재하지 않으면 생성
log_dir = os.path.dirname(LOG_FILE)

if not os.path.exists(log_dir):
    os.makedirs(log_dir)