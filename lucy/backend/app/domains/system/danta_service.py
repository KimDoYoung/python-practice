
from datetime import datetime
from typing import List

from pydantic import BaseModel
from backend.app.managers.stock_api_manager import StockApiManager
from dependency import get_user_service

class DantaStock(BaseModel):
    stk_code: str
    stk_name: str
    buy_price: int
    buy_time : str
    sell_price: int
    sell_time: str

class DantaService:
    def __init__(self, user_id, stock_abbr) -> None:
        self.user_id = user_id
        self.stk_abbr = stock_abbr
        self.user_service = get_user_service()
        

    async def initialize(self):
        self.user = await self.user_service.get_1(self.user_id)
        self.stockApi = await StockApiManager().stock_api(self.stk_abbr)
        self.lsapi = await StockApiManager().stock_api('LS')
        self.kisapi = await StockApiManager().stock_api('KIS')
        
    async def is_market_open_day(self, now: datetime):
        ''' 오늘이 개장일이면 True 아니면 False '''
        now_ymd = now.strftime("%Y%m%d")
        resp = self.kisapi.chk_workingday(now_ymd)        
        for item in resp.output:
            if item.opnd_yn == 'Y' and item.bass_dt == now_ymd:
                return True
        return False
    
    async def choice_danta_stocks(self) -> List[DantaStock]:
        return '005930'
    
    async def get_available_money(self):
        return 1000000
    
    async def sell_decision(self, stock):
        current_price = await self.get_current_price(stock)
        # 손절 또는 익절 조건을 판단 (예시)
        if current_price > self.buy_price[stock] * 1.05:  # 예: 5% 이상 상승 시 익절
            return '익절'
        elif current_price < self.buy_price[stock] * 0.95:  # 예: 5% 이상 하락 시 손절
            return '손절'
        return '보유'
    
    async def buy(self, stock, money):
        # money 가 1000이면 1000원 이하에서 가능한 주식수를 계산해서 구매
        pass
    
    async def sell(self, stock):
        # stock을 매도
        pass