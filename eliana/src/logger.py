# logger.py
import logging
from logging.handlers import TimedRotatingFileHandler
import os
from constants import ELIANA_MODE, LOG_FILE_NAME

log_file_path = LOG_FILE_NAME

def get_logger(name):
    logger = logging.getLogger(name)
    
    if ELIANA_MODE == "LOCAL":
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.ERROR)
        
    if not logger.handlers:
        # 매일 자정에 로그 파일을 회전, 최대 7개의 파일 보관
        file_handler = TimedRotatingFileHandler(log_file_path, when="midnight", interval=1, backupCount=7)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
    return logger
