
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from backend.app.domains.stc.kis.model.kis_order_cash_model import OrderCash_Request
from backend.app.domains.stc.ls_interface_model import Order_Request
from backend.app.managers.stock_api_manager import StockApiManager
from backend.app.core.dependency import get_log_service, get_mystock_service, get_user_service
from backend.app.utils.ls_model_util import order_to_cspat00601_Request

from backend.app.core.logger import get_logger
logger = get_logger(__name__)

class DantaStock(BaseModel):
    stk_code: str # 종목코드
    stk_name: str # 종목명
    buy_ordno : Optional[str] = '' # 매수주문번호
    buy_qty : Optional[int] = 0 # 매수수량
    buy_price: Optional[int] = 0 # 매수가격
    buy_time : Optional[str] = '' # 매수시간
    sell_ordno: Optional[str] = '' # 매도주문번호
    sell_qty : Optional[int] = 0 # 매도수량
    sell_price: Optional[int] = 0  # 매도가격
    sell_time: Optional[str] = '' # 매도시간

class DantaService:
    def __init__(self, user_id, stock_abbr) -> None:
        self.user_id = user_id
        self.stk_abbr = stock_abbr
        self.user_service = get_user_service()
        self.log_service = get_log_service()
        self.mystock_service = get_mystock_service()
        self.cache = {} # 캐시
        self.cache['holiday'] = {} # 휴일 캐시
        

    async def initialize(self):
        self.user = await self.user_service.get_1(self.user_id)
        self.lsapi = await StockApiManager().stock_api('LS')
        self.kisapi = await StockApiManager().stock_api('KIS')
        if self.stk_abbr == 'LS':
            self.defaultApi = self.lsapi
        elif self.stk_abbr == 'KIS':
            self.defaultApi = self.kisapi
        await self.log_service.danta_info(f'{self.user_id}의 단타서비스 초기화 완료')
                
    async def is_market_open_day(self, now: datetime):
        ''' 오늘이 개장일이면 True 아니면 False '''
        now_ymd = now.strftime("%Y%m%d")
        # cache에서 먼저 찾는다.
        result_in_cache = self.cache['holiday'].get(now_ymd)
        if result_in_cache is not None:
            return result_in_cache
        
        resp = await self.kisapi.chk_workingday(now_ymd)        
        for item in resp.output:
            if item.opnd_yn == 'Y' and item.bass_dt == now_ymd:
                self.cache['holiday'][now_ymd] = True
                return True
        self.cache['holiday'][now_ymd] = False
        return False
    
    async def get_current_price(self, stk_code:str):
        ''' stk_code의 현재가격 '''
        cost = await self.kisapi.get_current_price(stk_code)
        return cost

    async def get_available_qty_cost(self, stk_code:str, money:int):
        ''' money의 범위 내에서 매수가능수량 '''
        current_cost = await self.get_current_price(stk_code)
        # current_cost * x + (current_cost * x * 0.04)  = money
        x = int(money / (current_cost * 1.04))
        if (x > 1):
            x = x - 1
        return x, current_cost
    
    async def load_danta_stock_from_db(self)-> List[DantaStock]:
        ''' DB에서 단타 주식을 가져온다. 결국 파는 것인가? '''
        danta_list = await self.mystock_service.get_all_by_type('단타')
        inquire_balance = await self.kisapi.inquire_balance()
        real_list = inquire_balance.output1
        
        list = []
        for item in danta_list:
            stock = DantaStock(stk_code=item.stk_code, stk_name=item.stk_name)
            # for real in real_list:
            #     if real.pdno == item.stk_code:
            #         stock.buy_qty = real.hqty
            #         stock.buy_price = real.pamt
            #         break
            list.append(stock)
        return list
        
    async def choice_danta_stocks(self) -> List[DantaStock]:
        ''' 단타 주식 선택 '''
        stocks = []
        stock = DantaStock(stk_code='004090', stk_name='한국석유')
        stocks.append(stock)
        stock = DantaStock(stk_code='032820', stk_name='우리기술')
        stocks.append(stock)
        stock = DantaStock(stk_code='255440', stk_name='야스')
        stocks.append(stock)
        return stocks
    
    async def choice_for_danta_condition(self)-> List[DantaStock]:
        ''' 조건식리스트를 1. 조회해서 2. 그것을 수행해서 3. 종목을 3개 골라서 mystock collection에 넣는다.'''
        # 1. 조건식리스트를 조회
        seq = await self.get_seq_of_danta_condition('단타종가')
        if seq is None:
            seq = '0'
        psearch_result = await self.kisapi.psearch_result(seq)
        list = psearch_result.output2
        
        # 2. mystock collection에서 단타종류를 모두 삭제 후 추가
        #await self.mystock_service.delete_all_by_type('단타')
        i = 0
        choice_stocks = []
        for item in list:
            stk_code = item.code
            stk_name = item.name
            price = item.price
            danta_stock = DantaStock(stk_code=stk_code, stk_name=stk_name, buy_price=price)
            choice_stocks.append(danta_stock)
            i = i + 1
            if i >= 3:
                break
        
        return choice_stocks
    
    async def get_available_money(self):
        ''' 단타머신이 사용할 최대 금액 '''
        return 120000
    
    async def sell_decision(self, stock: DantaStock):
        current_price = await self.get_current_price(stock.stk_code)
        # 손절 또는 익절 조건을 판단 (예시)
        if current_price > (stock.buy_price * 1.03):  # 예: 5% 이상 상승 시 익절
            return '익절'
        elif current_price < (stock.buy_price * 0.97):  # 예: 5% 이상 하락 시 손절
            return '손절'
        return '보유'
    
    async def buy(self, stock: DantaStock, cost:int, qty:int):
        ''' stock을  cost가격에 qty만큼 매수 '''
        if self.stk_abbr == 'LS':
            #LS API를 이용해서 주식을 매수
            order_req = Order_Request(buy_sell_gb="매수", stk_code=stock.stk_code, qty=qty, price=0) 
            req = order_to_cspat00601_Request(order_req)
            resp = await self.lsapi.order(req)
            if resp.rsp_cd.startswith('00'):
                stock.buy_qty = qty
                stock.buy_price = cost # TODO: 체결가격은 아니고 현재가
                stock.buy_ordno = resp.CSPAT00601OutBlock2.OrdNo
                stock.buy_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                title = f'매수주문 성공: {stock.stk_name} {stock.buy_qty}주, 주문번호: {stock.buy_ordno}'
                self.log_service.danta_info(title=title)
            else:
                title = f'매수주문 실패: {stock.stk_name}, {resp.msg1}'
                self.log_service.danta_error(title=title)                            
        elif self.stk_abbr == 'KIS':
            # KIS API를 이용해서 주식을 매수
            order_req = OrderCash_Request(buy_sell_gb="매수", stk_code=stock.stk_code, qty=qty, price=0)
            resp = await  self.kisapi.order(order_req)
            if resp.rt_cd.startswith('0'):
                await self.log_service.danta_info(f'매수주문 성공: {stock.stk_name} {qty}주, 주문번호: {resp.output.KRX_FWDG_ORD_ORGNO}')
                stock.buy_qty = qty
                stock.buy_price = cost # TODO: 체결가격은 아니고 현재가
                stock.buy_ordno = resp.output.KRX_FWDG_ORD_ORGNO
                stock.buy_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                title = f'매수주문 성공: {stock.stk_name} {stock.buy_qty}주, 주문번호: {stock.buy_ordno}'
                await self.log_service.danta_info(title=title)
            else:
                title = f'매수주문 실패: {stock.stk_name}, {resp.msg1}'
                await self.log_service.danta_error(title=title)
    
    async def sell(self, stock:DantaStock, sell_price=0):
        '''sell_price에 매도, sellprice가 0이면 현재가로 매도'''
        qty = stock.buy_qty
        if self.stk_abbr == 'LS':            
            order_req = Order_Request(buy_sell_gb="매도", stk_code=stock.stk_code, qty=qty) 
            req = order_to_cspat00601_Request(order_req)
            resp  = await self.lsapi.order(req)
            if resp.rsp_cd.startswith('00'):
                stock.sell_qty = qty
                stock.sell_price = sell_price # TODO: 체결가격은 아니고 현재가
                stock.sell_ordno = resp.CSPAT00601OutBlock2.OrdNo
                stock.sell_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                title = f'매도주문 성공: {stock.stk_name} {stock.buy_qty}주, 주문번호: {stock.buy_ordno}'
                await self.log_service.danta_info(title=title)
            else:
                title = f'매도주문 실패: {stock.stk_name}, {resp.msg1}'
                await self.log_service.danta_error(title=title)                            
        else:
            order_req = OrderCash_Request(buy_sell_gb="매도", stk_code=stock.stk_code, qty=qty)
            resp = await self.kisapi.order(order_req)
            if resp.rt_cd.startswith('0'):
                stock.sell_qty = qty
                stock.sell_price = sell_price # TODO: 체결가격은 아니고 현재가
                stock.sell_ordno = resp.output.KRX_FWDG_ORD_ORGNO
                stock.sell_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                title = f'매도주문 성공: {stock.stk_name} {stock.sell_qty}주, 주문번호: {stock.sell_ordno}'
                await self.log_service.danta_info(title=title)
            else:
                title = f'매도주문 실패: {stock.stk_name}, {resp.msg1}'
                await self.log_service.danta_error(title=title)
    
    async def get_seq_of_danta_condition(self, condition_nm:str):
        ''' 조건식리스트를 가져온다'''
        title_result = await self.kisapi.psearch_title()
        rt_cd = title_result.rt_cd
        if rt_cd == '0':
            list = title_result.output2
            for item in list:
                if item.condition_nm == condition_nm:
                    return item.seq
        return None
    
