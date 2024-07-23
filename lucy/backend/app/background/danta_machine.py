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
from datetime import datetime, time
import asyncio

from beanie import init_beanie
from backend.app.core.config import config
from backend.app.core.logger import get_logger
from backend.app.domains.system.danta_service import DantaService
from backend.app.domains.user.user_model import User

logger = get_logger(__name__)
# 단타 머신 Task
Danta_Machine_Task = None

async def start_danta_machine():
    ''' 단타 머신 시작 '''
    global Danta_Machine_Task
    if Danta_Machine_Task is None or Danta_Machine_Task.cancelled():
        Danta_Machine_Task = asyncio.create_task(danta_machine_main())
        logger.info("단타머신 시작")


async def stop_danta_machine():
    ''' 단타 머신 종료 '''
    global Danta_Machine_Task
    if Danta_Machine_Task:
        Danta_Machine_Task.cancel()
        try:
            await Danta_Machine_Task
        except asyncio.CancelledError as e:
            logger.error(f"단타머신 종료 중 에러 발생: {e}")
        finally:
            Danta_Machine_Task = None
        logger.info("단타머신 종료")

def danta_machine_status() -> str:
    global Danta_Machine_Task
    if Danta_Machine_Task is None or Danta_Machine_Task.cancelled():
        return "stopped"
    else:
        return "running"

async def danta_machine_main():
    '''' 단타 머신 메인 루프 '''
    service = DantaService(config.DEFAULT_USER_ID, config.DEFAULT_STOCK_ABBR)
    await service.initialize()
    
    stocks = []
    stock_choice_done = False
    while True:
        now = datetime.now()
        # 주식 시장이 열리는 날이 아니면 1시간 후에 다시 체크
        market_open_day = await service.is_market_open_day(now)
        market_open_time = False
        if market_open_day and ( time(9, 0) <= now.time() <= time(15, 30)):
            market_open_time = True
        market_close_day = not market_open_day
        market_close_time = not market_open_time
        
        if market_close_day:
            await asyncio.sleep(60 * 60 * 60) # 1시간 후에 다시 체크
            continue
        
        # 시장이 열리는 시간 내에만 동작
        if market_close_time:
            await asyncio.sleep(60 * 60 * 60)  # 시장이 닫힌 시간에는 1시간마다 체크
            continue        
        
        # if not stock_choice_done and market_open_time and now.hour == 9 and now.minute == 1:
        if not stock_choice_done and market_open_time:
            stocks = await service.choice_danta_stocks() 
            total_money = await service.get_available_money()
            for stock in stocks:
                await service.buy_within_money(stock, int(total_money/len(stocks)))
            stock_choice_done = True    
            
        if stock_choice_done and now.hour == 15 and  now.minute > 25:
            # 3:25까지 매도하지 않은게 있다면 모두 매도
            for stock in stocks:
                await service.sell(stock)
            stocks = []
            stock_choice_done = False
            
        if stock_choice_done :
            # 매도 결정
            for stock in stocks:
                decision = await service.sell_decision(stock)
                if decision == '손절' or decision == '익절':
                    await service.sell(stock)
                    stocks.remove(stock)

        await asyncio.sleep(60*1) # 3분마다 현재 시간 체크        

async def db_init():
    from backend.app.core.mongodb import MongoDb
    mongodb_url = config.DB_URL 
    db_name = config.DB_NAME
    logger.info(f"MongoDB 연결: {mongodb_url} / {db_name}")
    await MongoDb.initialize(mongodb_url)
    
    db = MongoDb.get_client()[db_name]
    await init_beanie(database=db, document_models=[User])
        

async def main():
    try:
        await db_init()
        await danta_machine_main()
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())