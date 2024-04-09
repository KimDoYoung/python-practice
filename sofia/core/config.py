# config.py
from dotenv import load_dotenv
import os

# 현재 환경에 맞는 .env 파일을 로드하는 함수
# def load_environment(env_mode):
#     dotenv_path = f'.env.{env_mode}'
#     load_dotenv(dotenv_path=dotenv_path)

# 환경 변수를 통해 현재 모드를 결정
env_mode = os.getenv('SOFIA_MODE', 'local')
print("=====================================  env_mode  =====================================")
print(f"env_mode: {env_mode}")
print("=====================================  env_mode  =====================================")
# load_environment(env_mode)
PROJECT_NAME="SOFIA"


if env_mode == "local":
    LOG_FILE = f"c:\\tmp\\logs\\{PROJECT_NAME.lower()}\\{PROJECT_NAME.lower()}.log"
else:  
    LOG_FILE=f"/logs/{PROJECT_NAME.lower()}/{PROJECT_NAME.lower()}.log"

# 로그파일폴더가 존재하지 않으면 생성
log_dir = os.path.dirname(LOG_FILE)

if not os.path.exists(log_dir):
    os.makedirs(log_dir)