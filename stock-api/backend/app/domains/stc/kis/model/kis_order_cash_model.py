from typing import Literal, Optional

from pydantic import BaseModel
from backend.app.domains.stock_api_base_model import StockApiBaseModel


# 주문 요청
class KisOrderCashRequest(BaseModel):
    ''' 주문 요청 '''
    buy_sell_gb: Literal['매수', '매도']
    user_id: str # 사용자 ID
    acctno: str # 계좌번호
    stk_code: str
    qty: int
    cost: int = 0 # cost가 0이면 시장가로 주문

class OrderCashItem(StockApiBaseModel):
    KRX_FWDG_ORD_ORGNO: str
    ODNO: str
    ORD_TMD: str

# 주문 응답
class KisOrderCashResponse(StockApiBaseModel):
    '''order_cash  결과'''
    rt_cd: str
    msg_cd: str
    msg1: str
    output: Optional[OrderCashItem] = None


class OrderRvsecnclItem(BaseModel):
    KRX_FWDG_ORD_ORGNO: str # 한국거래소전송주문조직번호 주문시 한국투자증권 시스템에서 지정된 영업점코드
    ODNO: str # 주문번호 정정 주문시 한국투자증권 시스템에서 채번된 주문번호
    ORD_TMD: str # 주문시각 주문시각(시분초HHMMSS)

# 주문취소 응답
class KisOrderCancelResponse(StockApiBaseModel):
    rt_cd: str # 성공 실패 여부 0 : 성공 0 이외의 값 : 실패
    msg_cd: str # 응답코드 응답코드
    msg1: str # 응답메세지 응답메세지
    output: OrderRvsecnclItem

# 주문취소 요청
class KisOrderCancelRequest(BaseModel):
    ord_gno_brno:str # 주문지점번호 주문시 한국투자증권 시스템에서 지정된 영업점코드
    orgn_odno:str # 원주문번호 정정 주문시 한국투자증권 시스템에서 채번된 주문번호
    ord_dvsn_cd:str # 주문구분코드 1 : 정상주문 2 : 정정주문 3 : 취소주문
    ord_unpr:str # 주문단가 주문단가