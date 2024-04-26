# config.py
from dotenv import load_dotenv
import os

class Config:
    def __init__(self):
        self.PROFILE_NAME = os.getenv('JOANNA_MODE', 'local')
        load_dotenv(dotenv_path=f'.env.{self.PROFILE_NAME}')
        host = os.getenv('DB_HOST', 'localhost')
        port = os.getenv('DB_PORT', 5432)
        user = os.getenv('DB_USER', 'kdy987')
        password = os.getenv('DB_PASSWORD')
        database = os.getenv('DB_DATABASE')
        self.DATABASE_URL = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"
        
        # 로그 설정
        self.LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')
        self.LOG_FILE = os.getenv('LOG_FILE', 'c:\\tmp\\logs\\joanna\\joanna.log')
        log_dir = os.path.dirname(self.LOG_FILE)

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

config = Config()
