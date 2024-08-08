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
from backend.app.domains.stc.kis.kis_ws_task import KISTask
from backend.app.domains.system.danta_service import DantaService
from backend.app.domains.system.logs_model import Logs
from backend.app.domains.user.user_model import User
from backend.app.core.dependency import get_user_service
from backend.app.managers.danta_ws_manager import DantaWsManager
from backend.app.utils.kis_ws_util import KIS_WSReq

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
    
async def danta_machine_main(event_queue: asyncio.Queue):
    
    one_min = 60
    one_hour = 60 * one_min
    service = DantaService(config.DEFAULT_USER_ID, config.DEFAULT_STOCK_ABBR)
    await service.initialize()
    
    today_danta_stocks = [] # 단타 매매할 주식 리스트
    user_service = get_user_service()
    user = await user_service.get_1( config.DEFAULT_USER_ID)
    account =  user.find_account_by_abbr(config.DEFAULT_STOCK_ABBR)
    acctno = account.account_no

    client_ws_manager = DantaWsManager(event_queue)
    # client_ws_manager.setEventQueue(event_queue)
    
    client_ws_manager.connect(None, config.DEFAULT_USER_ID)
    kis_task = KISTask(config.DEFAULT_USER_ID, acctno, client_ws_manager)
    await kis_task.initialize()
    # kis_task.run()을 별도의 비동기 작업으로 실행
    asyncio.create_task(kis_task.run())
    
    while True:
        # 현재시간을 구하면서 시작
        now = datetime.now()
        logger.debug(f"현재시간: {now}")

        # 변수들 셋팅
        danta_stock_exists = len(today_danta_stocks) > 0 # 주식 선택이 완료되었는지 여부
        market_open_day = await service.is_market_open_day(now) # 주식 시장이 열려있는 날인지 여부
        market_open_time = False # 주식 시장이 열려있는 시간인지 여부
        if market_open_day and ( time(9, 0) <= now.time() <= time(15, 30)):
            market_open_time = True
        market_close_day = not market_open_day
        market_close_time = not market_open_time
        
        if market_close_day:
            await asyncio.sleep(one_hour * 1) 
            continue
        
        if market_close_time:
            await asyncio.sleep(one_min) 
            continue
        
        #1. 오전에 단타매매할 주식을  MyStocks에서 가져온 후 호가등록을 한다
        if  not danta_stock_exists and market_open_time:
            
            today_danta_stocks = await service.choice_danta_stocks()
            # 호가등록
            for stock in today_danta_stocks:
                await kis_task.subscribe(KIS_WSReq.BID_ASK, stock.stk_code)
                
        # 이벤트 큐에서 메시지 읽기
        try:
            event = await event_queue.get()
            # 이벤트 처리 로직
            if event.get('type') == 'SELL_SIGNAL':
                stock_to_sell = event.get('data')
                stk_codes = stock_to_sell['stk_codes']
                for stk_code in stk_codes:
                    danta_stock = today_danta_stocks.find(lambda x: x.stk_code == stk_code)
                    await service.sell(danta_stock, sell_price=0)
        except asyncio.QueueEmpty:
            logger.debug('이벤트 큐가 비어있음')
            pass        
        
        await asyncio.sleep(one_min)
        
        #2. 가져온 주식에 대해서 WebSocket을 통해 실시간 호가 및 체결가를 가져온다.
        
        #3. 가져온 호가 및 체결가를 분석하여 매수/매도를 한다.
        
        #4. 시간이 되면 모두 매도한다.
        
        #5. 매수할 조건의 주식을 선별한다.
        # if not danta_stock_exists and market_open_time: 
        #     try:
        #         today_danta_stocks = await service.choice_danta_stocks() 
        #         total_money = await service.get_available_money()
        #         for stock in today_danta_stocks:
        #             money = int(total_money / len(today_danta_stocks))
        #             qty, current_cost = await service.get_available_qty_cost(stock.stk_code, money)
        #             await service.buy(stock, cost=current_cost, qty=qty)
        #         danta_stock_exists = True
        #         logger.debug("오늘의 매수 주식을 선별해서 매수하였습니다.")
        #     except Exception as e:
        #         logger.error(f"선별 및 매수 중 오류: {e}")
        
        
#TODO : Websocket을 어떻게 붙일 수 있을까?
#TODO : 매수/매도를 해 볼것
#TODO : 종가배팅이어야한다.
async def danta_machine_main1():
    '''' 단타 머신 메인 루프 '''
    one_min = 60
    one_hour = 60 * one_min
    service = DantaService(config.DEFAULT_USER_ID, config.DEFAULT_STOCK_ABBR)
    await service.initialize()
    
    danta_stocks = [] # 단타 매매할 주식 리스트
    
    while True:
        # 현재시간을 구하면서 시작
        now = datetime.now()
        # 변수들 셋팅
        stock_choice_done = len(danta_stocks) > 0 # 주식 선택이 완료되었는지 여부
        market_open_day = await service.is_market_open_day(now) # 주식 시장이 열려있는 날인지 여부
        market_open_time = False # 주식 시장이 열려있는 시간인지 여부
        if market_open_day and ( time(9, 0) <= now.time() <= time(15, 30)):
            market_open_time = True
        market_close_day = not market_open_day
        market_close_time = not market_open_time
        
        # 주식 시장이 열리는 날이 아니거나 장시간이 지났다면 1시간쉬고 다시 시작
        if market_close_day:
            await asyncio.sleep(one_hour * 6) 
            continue
        
        if market_open_day and market_close_time:
            if time(0, 0 ) <= now.time() <= time(8,30):
                await asyncio.sleep(one_hour) 
            elif time(16, 00) <= now.time() <= time(23,59):
                await asyncio.sleep(one_hour) 
            else:
                await asyncio.sleep(one_min * 5)
            continue
        
        # 단타매매할 주식을 고른다.
        if not stock_choice_done and market_open_time: 
            try:
                danta_stocks = await service.choice_danta_stocks() 
                total_money = await service.get_available_money()
                for stock in danta_stocks:
                    money = int(total_money / len(danta_stocks))
                    qty, current_cost = await service.get_available_qty_cost(stock.stk_code, money)
                    await service.buy(stock, cost=current_cost, qty=qty)
                stock_choice_done = True
                logger.debug("오늘의 매수 주식을 선별해서 매수하였습니다.")
            except Exception as e:
                logger.error(f"선별 및 매수 중 오류: {e}")        
        
        # 단타매매할 주식이 있고 장 끝날 시간이면 모두 매도한다.    
        if stock_choice_done and now.hour > 14 and  now.minute > 18:
            # 3:25까지 매도하지 않은게 있다면 모두 매도
            for stock in danta_stocks:
                current_cost = await service.get_current_price(stock.stk_code)
                await service.sell(stock, sell_price=current_cost)
            danta_stocks = []
            stock_choice_done = False
        
        # 단타매매 주식이 있다면 3분마다 매도 결정      
        if stock_choice_done :
            # 매도 결정
            for stock in danta_stocks:
                decision = await service.sell_decision(stock)
                if decision == '손절' or decision == '익절':
                    current_cost = await service.get_current_price(stock.stk_code)
                    await service.sell(stock, sell_price=current_cost)
                    danta_stocks.remove(stock)        
        
        stock_choice_done = len(danta_stocks) > 0 # 주식을 모두 팔았다면 
        if not stock_choice_done:
            # 종료한다.
            break
        await asyncio.sleep(one_min*3) # 3분마다 현재 시간 체크        

async def db_init():
    from backend.app.core.mongodb import MongoDb
    mongodb_url = config.DB_URL 
    db_name = config.DB_NAME
    logger.info(f"MongoDB 연결: {mongodb_url} / {db_name}")
    await MongoDb.initialize(mongodb_url)
    
    db = MongoDb.get_client()[db_name]
    await init_beanie(database=db, document_models=[User])
    await init_beanie(database=db, document_models=[Logs])
        

async def main():
    event_queue = asyncio.Queue()
    try:
        await db_init()
        await danta_machine_main(event_queue)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        await asyncio.sleep(0.1)  # 모든 비동기 작업이 완료되도록 약간의 시간을 둠        

if __name__ == "__main__":
    asyncio.run(main())