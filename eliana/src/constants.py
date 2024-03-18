# constants.py
from dotenv import load_dotenv
import os

# .env 파일의 내용을 로드합니다.
load_dotenv()

# 환경변수를 읽어와서 상수에 할당합니다.
ELIANA_MODE = os.getenv('ELIANA_MODE', 'LOCAL')
ELINA_PORT=int(os.getenv('ELINA_PORT', 8989))

# ELIANA_MODE 값에 따라 CHART_BASE_URL을 설정합니다.
if ELIANA_MODE == "LOCAL":
    CHART_BASE_URL = f"http://localhost:{ELINA_PORT}"
    LOG_FILE_NAME = os.path.join("c:\\tmp\\logs\\eliana.log")
else:  # ELIANA_MODE가 "REAL"일 경우, 실제 운영 환경의 URL을 사용합니다.
    CHART_BASE_URL = "https://localhost:{ELINA_PORT}"
    LOG_FILE_NAME="/log/elianna.log"

LOG_DIR = os.path.dirname(LOG_FILE_NAME)  # 로그 파일의 부모 디렉터리 경로 추출

# 해당 디렉터리가 없으면 생성
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR, exist_ok=True)    