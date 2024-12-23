# Python 3.12.2 이미지 사용
FROM python:3.12.2-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필수 시스템 패키지 설치 (Chrome 설치)
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    chromium \
    --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Python 패키지 설치
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY kind_scrapy.py .

# tmp와 data 폴더 생성
RUN mkdir -p tmp data

# 환경 변수 설정
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:99

# 컨테이너 대기 상태 유지
CMD ["tail", "-f", "/dev/null"]
