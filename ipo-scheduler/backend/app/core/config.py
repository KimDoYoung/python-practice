from dotenv import load_dotenv
import os
class Config:
    def __init__(self):
        self.PROFILE_NAME = os.getenv('IPO_SCHEDULER_MODE', 'local')
        load_dotenv(dotenv_path=f'.env.{self.PROFILE_NAME}')
        
        # 디폴트사용자
        self.DEFAULT_USER_ID = os.getenv('DEFAULT_USER_ID', 'kdy987')
        self.DEFAULT_STOCK_ABBR = os.getenv('DEFAULT_STOCK_ABBR','KIS')

        # DB 설정
        self.DB_URL = os.getenv('DB_URL', 'mongodb://root:root@test.kfs.co.kr:27017/')
        self.DB_NAME = os.getenv('DB_NAME', 'ipo-schedule')

        # 로그 설정
        self.LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')
        self.LOG_FILE = os.getenv('LOG_FILE', './logs/ipo-schduler.log')

        self.SECRET_KEY = os.getenv('SECRET_KEY','ipo_schduler_secret_key_1234_!@#$')
        self.ALGORITHM = os.getenv('ALGORITHM','HS256')
        self.ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 30)
        self.ACCESS_TOKEN_NAME = os.getenv('ACCESS_TOKEN_NAME', 'ipo_schduler_token')
        
        self.DATA_FOLDER = os.getenv('DATA_FOLDER', './data')
        self.FILE_FOLDER = os.getenv('FILE_FOLDER', './files')

        # 로그 디렉토리 생성
        log_dir = os.path.dirname(self.LOG_FILE)

        # DATA_FOLDER 디렉토리 생성
        if not os.path.exists(self.DATA_FOLDER):
            os.makedirs(self.DATA_FOLDER)
        
        if not os.path.exists(self.FILE_FOLDER):
            os.makedirs(self.FILE_FOLDER)

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

config = Config()