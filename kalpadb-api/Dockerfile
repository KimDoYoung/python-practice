# ----------------------------------------------------
# Dockerfile for kalpadb-api with Selenium and JDK 1.8
# ----------------------------------------------------
FROM python:3.12-slim

# 필수 패키지 업데이트 및 설치
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    default-jdk \
    libnss3 \
    libgconf-2-4 \
    xvfb \
    gnupg \
    --no-install-recommends \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 환경 변수 설정
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

# Chrome 설치
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get update \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb

# ChromeDriver 설치 (Chrome 버전과 일치)
RUN CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+') \
    && CHROME_DRIVER_VERSION=$(wget -qO- "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION") \
    && wget -q "https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip" \
    && unzip chromedriver_linux64.zip -d /usr/local/bin/ \
    && rm chromedriver_linux64.zip \
    && chmod +x /usr/local/bin/chromedriver

# 환경 변수 추가
ENV CHROME_BIN=/usr/bin/google-chrome
ENV PATH=$PATH:/usr/bin
ENV DISPLAY=:99

# Python 패키지 설치
RUN pip install --upgrade pip

# 작업 디렉토리 설정
WORKDIR /kalpadb-api

# 필요한 라이브러리 설치를 위해 requirements.txt 파일을 복사
COPY . .

# 의존성 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# FastAPI 실행 (main.py에서 FastAPI 객체를 정의했을 때의 파일 경로)
CMD ["xvfb-run", "--server-args=-screen 0 1024x768x24", "uvicorn", "app.kalpadb-api-main:app", "--host", "0.0.0.0", "--port", "8088", "--log-level", "debug"]
