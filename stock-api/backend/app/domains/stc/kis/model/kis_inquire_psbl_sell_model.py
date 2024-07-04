from backend.app.domains.stock_api_base_model import KisBaseModel
# 매도 가능수량 조회
class InquirePsblSellItem(KisBaseModel):
    pdno: str # 상품번호 
    prdt_name: str # 상품명 
    buy_qty: str # 매수수량 
    sll_qty: str # 매도수량 
    cblc_qty: str # 잔고수량 
    nsvg_qty: str # 비저축수량 
    ord_psbl_qty: str # 주문가능수량 
    pchs_avg_pric: str # 매입평균가격 
    pchs_amt: str # 매입금액 
    now_pric: str # 현재가 
    evlu_amt: str # 평가금액 
    evlu_pfls_amt: str # 평가손익금액 
    evlu_pfls_rt: str # 평가손익율 

class InquirePsblSellDto(KisBaseModel):
    rt_cd: str # 성공 실패 여부 
    msg_cd: str # 응답코드 
    msg1: str # 응답메세지 
    output1: InquirePsblSellItem