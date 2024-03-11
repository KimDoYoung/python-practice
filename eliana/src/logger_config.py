import logging
import os
from logging.handlers import TimedRotatingFileHandler

log_directory = "log"
log_file_name = "eliana.log"
log_file_path = os.path.join(log_directory, log_file_name)

# log 폴더가 없으면 생성
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG) # 로그 레벨 설정
    if not logger.handlers:
        # 매일 자정에 로그 파일을 회전, 최대 7개의 파일 보관
        file_handler = TimedRotatingFileHandler(log_file_path, when="midnight", interval=1, backupCount=7)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger
