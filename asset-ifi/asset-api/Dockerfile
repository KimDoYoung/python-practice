# ----------------------------------------------------
# Dockerfile for asset-api
# ----------------------------------------------------
# 베이스 이미지 설정
FROM python:3.12-slim

RUN pip install --upgrade pip

# 작업 디렉토리 설정
WORKDIR /

# 필요한 라이브러리 설치를 위해 requirements.txt 파일을 복사
COPY . .

# 의존성 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# FastAPI 실행 (main.py에서 FastAPI 객체를 정의했을 때의 파일 경로)
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info"]
