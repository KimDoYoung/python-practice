import logging
from logging.handlers import RotatingFileHandler
import os


def get_logger(name):

    LOG_FILE = "c:\\tmp\\logs\\sofia\\sofia.log"
    # LOG_FILE의 디렉토리 경로를 얻음
    log_dir = os.path.dirname(LOG_FILE)

    # 해당 디렉토리가 존재하지 않으면 생성
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    logger = logging.getLogger(name)
    SOFIA_MODE = 'local'
    if SOFIA_MODE == "local":
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.ERROR)

    if not logger.handlers:
        # 매일 자정에 로그 파일을 회전, 최대 7개의 파일 보관
        # 파일의 최대 크기는 예시로 10MB로 설정하였습니다. 필요에 따라 조절하십시오.
        file_handler = RotatingFileHandler(LOG_FILE, "a", 10*1024*1024, 7)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        if SOFIA_MODE == "local":
            # 콘솔에도 로그 메시지 출력
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

    return logger