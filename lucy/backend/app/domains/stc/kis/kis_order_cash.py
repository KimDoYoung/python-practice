from typing import List, Literal

from pydantic import BaseModel, constr, field_validator, validator
from backend.app.domains.stc.kis.kis_base_model import KisBaseModel

'''
주식 주문내역 조회
'''

class OrderCashDto(BaseModel):
    buy_sell_gb: Literal['매수', '매도']
    stk_code: str
    qty: int

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

class KisOrderCash(KisBaseModel):
    '''order_cash 조회 결과'''
    rt_cd: str
    msg_cd: str
    msg1: str
    output: OrderCashItem