# logger.py
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
from logging.handlers import RotatingFileHandler
import os

def get_logger(name):
    from app.core.settings import config
    
    logger = logging.getLogger(name)
    logger.setLevel(config.LOG_LEVEL)
    LOG_FILE = config.LOG_FILE

    # 핸들러가 없을 경우에만 추가하여 중복을 방지합니다.
    if not logger.handlers:
        # 로그 디렉터리가 없으면 생성합니다.
        log_dir = os.path.dirname(LOG_FILE)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # RotatingFileHandler 설정: 파일 크기가 5MB를 초과하면 회전하고, 백업을 7개까지 보관합니다.
        file_handler = RotatingFileHandler(
            LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=7, encoding="utf-8"
        )
        
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        
        # 핸들러를 로거에 추가
        logger.addHandler(file_handler)

        # 로컬 환경일 경우 콘솔에도 로그 출력
        if config.PROFILE_NAME == "local":
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

    return logger

# def get_logger(name):
    
#     from app.core.settings import config
    
#     logger = logging.getLogger(name)
#     logger.setLevel(config.LOG_LEVEL)
#     LOG_FILE = config.LOG_FILE

#     if not logger.handlers:
#         # 일별 로그 회전. 매일 자정에 로그를 회전시키고, 최대 7일간 로그를 보관합니다.
#         log_dir = os.path.dirname(LOG_FILE)
#         if not os.path.exists(log_dir):
#             os.makedirs(log_dir)
        
#         # TimedRotatingFileHandler로 일자별 로그 파일 생성
#         file_handler = TimedRotatingFileHandler(
#             LOG_FILE, when="midnight", interval=1, backupCount=365, encoding="utf-8"
#         )
#         file_handler.suffix = "%Y-%m-%d"  # 로그 파일에 날짜 추가 (YYYY-MM-DD 형식)
#         file_handler.extMatch = r"^\d{4}-\d{2}-\d{2}$"  # 날짜에 맞는 형식 정의
#         formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
#         file_handler.setFormatter(formatter)
#         logger.addHandler(file_handler)
        
#         file_handler.close()

#         # 로컬 환경일 경우 콘솔에도 로그 출력
#         if config.PROFILE_NAME == "local":
#             console_handler = logging.StreamHandler()
#             console_handler.setFormatter(formatter)
#             logger.addHandler(console_handler)

#     return logger
