FROM python:3.12-slim

# 필수 패키지 설치
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    default-jdk \
    libnss3 \
    libgconf-2-4 \
    xvfb \
    gnupg \
    xauth \
    libx11-xcb1 \
    libxcomposite1 \
    libxi6 \
    libxrandr2 \
    libxdamage1 \
    libxtst6 \
    libasound2 \
    libatk-bridge2.0-0 \
    libcups2 \
    --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Chrome 설치
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get update \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb

# ChromeDriver 설치
RUN CHROME_DRIVER_VERSION=$(wget -qO- https://chromedriver.storage.googleapis.com/LATEST_RELEASE) \
    && wget -q https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip -d /usr/local/bin/ \
    && rm chromedriver_linux64.zip \
    && chmod +x /usr/local/bin/chromedriver

# 환경 변수 설정
ENV CHROME_BIN=/usr/bin/google-chrome
ENV PATH=$PATH:/usr/bin
ENV DISPLAY=:99

# Python 설치
RUN pip install --upgrade pip

# 작업 디렉토리 설정
WORKDIR /kalpadb-api

# 코드 복사 및 종속성 설치
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# FastAPI 실행
#CMD ["xvfb-run", "--server-args=-screen 0 1024x768x24", "uvicorn", "app.kalpadb-api-main:app", "--host", "0.0.0.0", "--port", "8088", "--log-level", "debug"]
ENTRYPOINT ["xvfb-run", "--server-args=-screen 0 1024x768x24", "uvicorn"]
CMD ["app.kalpadb-api-main:app", "--host", "0.0.0.0", "--port", "8088", "--log-level", "debug"]

