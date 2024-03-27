import logging
from logging.handlers import TimedRotatingFileHandler

from backend.app.core.configs import LOG_FILE, MERIAN_PROFILE

def get_logger(name):
    logger = logging.getLogger(name)

    if MERIAN_PROFILE == "local":
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.ERROR)

    if not logger.handlers:
        # 매일 자정에 로그 파일을 회전, 최대 7개의 파일 보관
        file_handler = TimedRotatingFileHandler(LOG_FILE, when="midnight", interval=1, backupCount=7)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        if MERIAN_PROFILE == "local":
            # 콘솔에도 로그 메시지 출력
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

    return logger