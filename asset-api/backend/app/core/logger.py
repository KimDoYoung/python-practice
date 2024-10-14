"""
모듈 설명: 
    - 로그 모듈을 정의
    - Settings ( Config )에 정의된 LOG_LEVEL, LOG_FILE을 사용하여 로그를 생성
    - 로그파일은 일별로 생성되며, 최대 365일간 보관

작성자: 김도영
작성일: 2024-10-04
버전: 1.0
"""
import logging
from logging.handlers import TimedRotatingFileHandler
import os

def get_logger(name):
    
    from backend.app.core.settings import config
    
    logger = logging.getLogger(name)
    logger.setLevel(config.LOG_LEVEL)
    LOG_FILE = config.LOG_FILE

    if not logger.handlers:
        # 로그 디렉토리가 없으면 생성
        log_dir = os.path.dirname(LOG_FILE)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # TimedRotatingFileHandler로 일자별 로그 파일 생성
        file_handler = TimedRotatingFileHandler(
            LOG_FILE, when="midnight", interval=1, backupCount=365, encoding="utf-8"
        )
        file_handler.suffix = "%Y-%m-%d"  # 로그 파일에 날짜 추가 (YYYY-MM-DD 형식)
        
        # 로그 포맷 설정
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        
        # 핸들러 추가
        logger.addHandler(file_handler)

        # 로컬 환경일 경우 콘솔에도 로그 출력
        if config.PROFILE_NAME == "local":
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

    return logger
