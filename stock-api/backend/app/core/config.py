from dotenv import load_dotenv
import os
class Config:
    def __init__(self):
        self.PROFILE_NAME = os.getenv('STOCK_API_MODE', 'local')
        load_dotenv(dotenv_path=f'.env.{self.PROFILE_NAME}')

        # DB 설정
        self.DB_URL = os.getenv('DB_URL', 'mongodb://root:root@test.kfs.co.kr:27017/')
        self.DB_NAME = os.getenv('DB_NAME', 'stock-api-db')

        # 로그 설정
        self.LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')
        self.LOG_FILE = os.getenv('LOG_FILE', './logs/stock-api.log')

        # 로그 디렉토리 생성
        log_dir = os.path.dirname(self.LOG_FILE)

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

config = Config()