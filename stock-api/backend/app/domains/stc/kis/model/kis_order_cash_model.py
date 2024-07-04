from typing import Literal, Optional

from pydantic import BaseModel, field_validator, model_validator
from backend.app.domains.stock_api_base_model import KisBaseModel

'''
주식 주문내역 조회
'''

class KisOrderCashRequest(BaseModel):
    buy_sell_gb: Literal['매수', '매도']
    user_id: str # 사용자 ID
    acctno: str # 계좌번호
    stk_code: str
    qty: int
    cost: int = 0 # cost가 0이면 시장가로 주문

class LsOrderCashRequest(BaseModel):
    buy_sell_gb: Literal['매수', '매도']
    user_id: str # 사용자 ID
    acctno: str # 계좌번호
    stk_code: str
    qty: int
    cost: int = 0 # cost가 0이면 시장가로 주문

class OrderCashRequest(BaseModel):
    ''' 주문 요청 '''
    stk_abbr: Literal['KIS', 'LS']  # 종목약명은 kis 또는 ls
    kis_order_cash: Optional[KisOrderCashRequest] = None
    ls_order_cash: Optional[LsOrderCashRequest] = None
    
    @model_validator(mode="before")
    def check_order_cash(cls, values):
        stk_abbr = values.get('stk_abbr')  # 종목약명 가져오기
        kis_order_cash = values.get('kis_order_cash')  # KIS 주문 정보 가져오기
        ls_order_cash = values.get('ls_order_cash')  # LS 주문 정보 가져오기

        # 종목약명이 'kis'인 경우 kis_order_cash가 반드시 있어야 함
        if stk_abbr == 'KIS' and not kis_order_cash:
            raise ValueError('종목약명이 kis일 경우 kis_order_cash가 반드시 제공되어야 합니다.')
        
        # 종목약명이 'ls'인 경우 ls_order_cash가 반드시 있어야 함
        if stk_abbr == 'LS' and not ls_order_cash:
            raise ValueError('종목약명이 ls일 경우 ls_order_cash가 반드시 제공되어야 합니다.')
        
        # kis_order_cash와 ls_order_cash가 동시에 제공되어서는 안 됨
        if kis_order_cash and ls_order_cash:
            raise ValueError('kis_order_cash와 ls_order_cash 중 하나만 제공되어야 합니다.')
        
        return values  # 모든 조건을 만족하면 값을 반환


class OrderCashDto(BaseModel):
    buy_sell_gb: Literal['매수', '매도']
    stk_code: str
    qty: int
    cost: int = 0 # cost가 0이면 시장가로 주문

    @field_validator('stk_code')
    def stk_code_must_be_six_digits(cls, value):
        if not value.isdigit() or len(value) != 6:
            raise ValueError('stk_code must be a 6-digit number')
        return value

    @field_validator('qty')
    def qty_must_be_in_range(cls, value):
        if not (1 <= value <= 100000):
            raise ValueError('qty must be between 1 and 100000')
        return value

    class Config:
        anystr_strip_whitespace = True
        min_anystr_length = 1

#  {"rt_cd":"0","msg_cd":"APBK0013","msg1":"주문 전송 완료 되었습니다.","output":{"KRX_FWDG_ORD_ORGNO":"06590","ODNO":"0000006555","ORD_TMD":"151059"}}

class OrderCashItem(KisBaseModel):
    KRX_FWDG_ORD_ORGNO: str
    ODNO: str
    ORD_TMD: str

# 주문 응답
class KisOrderCash(KisBaseModel):
    '''order_cash 조회 결과'''
    rt_cd: str
    msg_cd: str
    msg1: str
    output: OrderCashItem

class LsOrderCash(KisBaseModel):
    '''order_cash 조회 결과'''
    rt_cd: str
    msg_cd: str
    msg1: str
    output: OrderCashItem    

class OrderCashResponse(KisBaseModel):
    stk_abbr: Literal['KIS', 'LS']
    KisOrderCashResponse: Optional[KisOrderCash] = None
    LsOrderCashResponse: Optional[LsOrderCash] = None


# 주문취소 응답
class OrderRvsecnclItem(BaseModel):
    KRX_FWDG_ORD_ORGNO: str # 한국거래소전송주문조직번호 주문시 한국투자증권 시스템에서 지정된 영업점코드
    ODNO: str # 주문번호 정정 주문시 한국투자증권 시스템에서 채번된 주문번호
    ORD_TMD: str # 주문시각 주문시각(시분초HHMMSS)

# 주문취소 응답
class OrderRvsecnclDto(KisBaseModel):
    rt_cd: str # 성공 실패 여부 0 : 성공 0 이외의 값 : 실패
    msg_cd: str # 응답코드 응답코드
    msg1: str # 응답메세지 응답메세지
    output: OrderRvsecnclItem

class OrderCancelRequest(BaseModel):
    ord_gno_brno:str # 주문지점번호 주문시 한국투자증권 시스템에서 지정된 영업점코드
    orgn_odno:str # 원주문번호 정정 주문시 한국투자증권 시스템에서 채번된 주문번호
    ord_dvsn_cd:str # 주문구분코드 1 : 정상주문 2 : 정정주문 3 : 취소주문
    ord_unpr:str # 주문단가 주문단가