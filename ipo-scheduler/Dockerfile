# ----------------------------------------------------
# Dockerfile for ipo-scheduler
# ----------------------------------------------------

# 베이스 이미지로3.10-slim 사용
FROM python:3.12-slim

# 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg2 \
    --no-install-recommends

# Google Chrome 설치
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable

# ChromeDriver 설치
RUN CHROME_DRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip

RUN pip install --upgrade pip

# 작업 디렉토리 설정
WORKDIR /

# 필요한 라이브러리 설치를 위해 requirements.txt 파일을 복사
COPY . .

# 의존성 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt


# FastAPI 실행 (main.py에서 FastAPI 객체를 정의했을 때의 파일 경로)
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "debug"]
