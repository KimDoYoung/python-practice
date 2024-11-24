# Python 3.9 Slim 이미지 사용
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필요 파일 복사
COPY ../requirements.txt /app/
COPY ap_file_wh.py /app/

# Python 종속성 설치
RUN pip install --no-cache-dir -r requirements.txt



