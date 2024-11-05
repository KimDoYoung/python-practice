import asyncio
from datetime import datetime
from backend.app.core.logger import get_logger
logger = get_logger(__name__)

def test_sync(msg: str):
    print("스케줄테스트>>> " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " : " + msg)
    return 1

# 간단한 비동기 테스트 함수 등록
async def test_async(arg):
    logger.info(f"테스트 simple_async_test is running with argument: {arg}")
    await asyncio.sleep(1)
    logger.info("simple_async_test completed")