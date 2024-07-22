from typing import Literal, Optional

from pydantic import BaseModel
from backend.app.domains.stock_api_base_model import StockApiBaseModel


# 주문 요청
class OrderCash_Request(BaseModel):
    ''' 주문 요청 '''
    buy_sell_gb: Literal['매수', '매도']
    user_id: Optional[str] = '' # 사용자 ID
    acctno: Optional[str] = '' # 계좌번호
    stk_code: str
    qty: int
    cost: int = 0 # cost가 0이면 시장가로 주문

class OrderCashItem(StockApiBaseModel):
    KRX_FWDG_ORD_ORGNO: str
    ODNO: str
    ORD_TMD: str

# 주문 응답
class KisOrderCash_Response(StockApiBaseModel):
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
class KisOrderCancel_Response(StockApiBaseModel):
    rt_cd: str # 성공 실패 여부 0 : 성공 0 이외의 값 : 실패
    msg_cd: str # 응답코드 응답코드
    msg1: str # 응답메세지 응답메세지
    output: OrderRvsecnclItem


# 주문취소 요청
class KisOrderCancel_Request(BaseModel):
    orgn_odno:str # 원주문번호 정정 주문시 한국투자증권 시스템에서 채번된 주문번호
    ord_dvsn_cd:str # 주문구분코드 1 : 정상주문 2 : 정정주문 3 : 취소주문
    ord_unpr:str # 주문단가 주문단가

class KisOrderRvsecncl_Request(StockApiBaseModel):
    ORGN_ODNO: str # 원주문번호 정정 주문시 한국투자증권 시스템에서 채번된 주문번호
    ORD_DVSN: str # 00 : 지정가
                # 01 : 시장가
                # 02 : 조건부지정가
                # 03 : 최유리지정가
                # 04 : 최우선지정가
                # 05 : 장전 시간외
                # 06 : 장후 시간외
                # 07 : 시간외 단일가
                # 08 : 자기주식
                # 09 : 자기주식S-Option
                # 10 : 자기주식금전신탁
                # 11 : IOC지정가 (즉시체결,잔량취소)
                # 12 : FOK지정가 (즉시체결,전량취소)
                # 13 : IOC시장가 (즉시체결,잔량취소)
                # 14 : FOK시장가 (즉시체결,전량취소)
                # 15 : IOC최유리 (즉시체결,잔량취소)
                # 16 : FOK최유리 (즉시체결,전량취소
    RVSE_CNCL_DVSN_CD: str #정정 : 01 취소 : 02"
    ORD_QTY: str # 주문수량 주문수량
    ORD_UNPR :str # 주문단가 주문단가
    QTY_ALL_ORD_YN :str # 전량주문여부 전량주문여부
    