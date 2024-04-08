import logging
import os
from concurrent_log_handler import ConcurrentRotatingFileHandler
from backend.app.core.configs import LOG_FILE

def get_logger(name):
    logger = logging.getLogger(name)
    JOANNA_MODE = os.getenv('JOANNA_MODE', 'local')
    if JOANNA_MODE == "local":
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.ERROR)

    if not logger.handlers:
        # 매일 자정에 로그 파일을 회전, 최대 7개의 파일 보관
        # 파일의 최대 크기는 예시로 10MB로 설정하였습니다. 필요에 따라 조절하십시오.
        file_handler = ConcurrentRotatingFileHandler(LOG_FILE, "a", 10*1024*1024, 7)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        if JOANNA_MODE == "local":
            # 콘솔에도 로그 메시지 출력
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

    return logger