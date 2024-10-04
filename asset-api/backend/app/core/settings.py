# settings.py
"""
모듈 설명: 
    - .env.{PROFILE_NAME} 파일을 로드하여 설정값을 가져옴
    - PROFILE_NAME 의 local과 real 2가지 모드를 지원
    - local 모드일 경우 .env.local 파일을 로드, real 모드일 경우 .env.real 파일을 로드
    - PROFILE_NAME 은 환경변수 AssetApi_Mode 로 설정

※주의: Config 라는 이름으로 다른 파일에서 사용하기로 함. 
        - config = Settings()
작성자: 김도영
작성일: 2024-10-04
버전: 1.0
"""
from dotenv import load_dotenv
import os
class Settings:
    def __init__(self):
        
        # PROFILE_NAME 환경변수를 읽어옴
        self.PROFILE = os.getenv('AssetApi_Mode', 'local')
        load_dotenv(dotenv_path=f'.env.{self.PROFILE}')
        
        # SERVICE설정
        self.SERVICE_TITLE = os.getenv('SERVICE_TITLE', 'AssetApi-한국펀드서비스 OPENAPI')
        self.SERVICE_PORT = os.getenv('SERVICE_PORT', 8000)
        
        # DB 설정
        db_host = os.getenv('DB_HOST', 'localhost')
        db_username = os.getenv('DB_USERNAME', 'kdy987')
        db_password = os.getenv('DB_PASSWORD', 'kalpa987!')
        db_port = os.getenv('DB_PORT', '5432')
        db_name = os.getenv('DB_NAME', 'assetapi')
        #"postgresql+asyncpg://user:password@localhost:5433/asset_api"
        self.DB_URL = f"postgresql+asyncpg://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"

        # JWT and Security
        self.AES_GLOBAL_KEY = os.getenv('AES_GLOBAL_KEY','kfs_assetapi_zaq1@WSX')   

        # 로그 설정
        self.LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')
        self.LOG_FILE = os.getenv('LOG_FILE', 'c:/tmp/logs/assetapi/AssetApi_Mode.log')


        # 로그 디렉토리 생성
        log_dir = os.path.dirname(self.LOG_FILE)

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

config = Settings()