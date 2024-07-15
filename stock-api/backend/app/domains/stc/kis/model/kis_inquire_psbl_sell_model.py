from typing import Optional
from backend.app.domains.stock_api_base_model import StockApiBaseModel
# 매도 가능수량 조회
class InquirePsblSellItem(StockApiBaseModel):
    pdno: Optional[str] = None  # 상품번호
    prdt_name: Optional[str] = None  # 상품명
    buy_qty: Optional[str] = None  # 매수수량
    sll_qty: Optional[str] = None  # 매도수량
    cblc_qty: Optional[str] = None  # 잔고수량
    nsvg_qty: Optional[str] = None  # 비저축수량
    ord_psbl_qty: Optional[str] = None  # 주문가능수량
    pchs_avg_pric: Optional[str] = None  # 매입평균가격
    pchs_amt: Optional[str] = None  # 매입금액
    now_pric: Optional[str] = None  # 현재가
    evlu_amt: Optional[str] = None  # 평가금액
    evlu_pfls_amt: Optional[str] = None  # 평가손익금액
    evlu_pfls_rt: Optional[str] = None  # 평가손익율

class InquirePsblSell_Response(StockApiBaseModel):
    rt_cd: str # 성공 실패 여부 
    msg_cd: str # 응답코드 
    msg1: str # 응답메세지 
    output: InquirePsblSellItem