# danta_machine.py
"""
모듈 설명: 
    - 자동으로 단타매매를 한다.
주요 기능:
    - 1. 조건식으로 오늘 단타를 칠 목록을 가져온다.
    - 2. 실시간으로 호가 및 체결가를 가져온다.
    - 3. 호가 및 체결가를 분석하여 매수/매도를 한다.

작성자: 김도영
작성일: 18
버전: 1.0
"""
import time
import asyncio
from backend.app.core.logger import get_logger

logger = get_logger(__name__)
# 단타 머신 Task
Danta_Machine_Task = None

async def start_danta_machine():
    global Danta_Machine_Task
    if Danta_Machine_Task is None or Danta_Machine_Task.cancelled():
        Danta_Machine_Task = asyncio.create_task(danta_machine_main())
        logger.info("단타머신 시작")
        #await send_danta_message("단타머신 시작합니다.")


async def stop_danta_machine():
    global Danta_Machine_Task
    if Danta_Machine_Task:
        Danta_Machine_Task.cancel()
        try:
            await Danta_Machine_Task
        except asyncio.CancelledError:
            logger.error("단타머신 종료 중 에러 발생")
            pass
        logger.info("단타머신 종료")
        #await send_danta_message("단타머신 종료합니다.")

async def danta_machine_main():
    '''' 단타 머신 메인 루프 '''
    while True:
        logger.debug("단타 머신 수행 중..." + str(time.time()))
        await asyncio.sleep(10)  # 실제 작업을 대체하는 지연
