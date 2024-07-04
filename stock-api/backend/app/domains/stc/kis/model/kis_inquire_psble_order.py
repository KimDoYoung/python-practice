
from pydantic import BaseModel
from backend.app.domains.stock_api_base_model import StockApiBaseModel
from typing import Optional

##############################################################################################
# [국내주식] 주문/계좌 > 매수가능조회
##############################################################################################

class InquirePsblOrderItem(StockApiBaseModel):
    ord_psbl_cash: str # 주문가능현금 
    ord_psbl_sbst: str # 주문가능대용 
    ruse_psbl_amt: str # 재사용가능금액 
    fund_rpch_chgs: str # 펀드환매대금 
    psbl_qty_calc_unpr: str # 가능수량계산단가 
    nrcvb_buy_amt: str # 미수없는매수금액 미수를 사용하지 않으실 경우 nrcvb_buy_amt(미수없는매수금액)을 확인
    nrcvb_buy_qty: str # 미수없는매수수량 미수를 사용하지 않으실 경우 nrcvb_buy_qty(미수없는매수수량)을 확인 * 특정 종목 전량매수 시 가능수량을 확인하실 경우  조회 시 ORD_DVSN:01(시장가)로 지정 필수 * 다만, 조건부지정가 등 특정 주문구분(ex.IOC)으로 주문 시 가능수량을 확인할 경우 주문 시와 동일한 주문구분(ex.IOC) 입력
    max_buy_amt: str # 최대매수금액 미수를 사용하시는 경우 max_buy_amt(최대매수금액)를 확인
    max_buy_qty: str # 최대매수수량 미수를 사용하시는 경우 max_buy_qty(최대매수수량)를 확인 * 특정 종목 전량매수 시 가능수량을 확인하실 경우  조회 시 ORD_DVSN:01(시장가)로 지정 필수 * 다만, 조건부지정가 등 특정 주문구분(ex.IOC)으로 주문 시 가능수량을 확인할 경우 주문 시와 동일한 주문구분(ex.IOC) 입력
    cma_evlu_amt: str # CMA평가금액 
    ovrs_re_use_amt_wcrc: str # 해외재사용금액원화 
    ord_psbl_frcr_amt_wcrc: str # 주문가능외화금액원화 

class InquirePsblOrderDto(StockApiBaseModel):
    rt_cd: str # 성공 실패 여부 0 : 성공 0 이외의 값 : 실패
    msg_cd: str # 응답코드 응답코드
    msg1: str # 응답메세지 응답메세지
    output: InquirePsblOrderItem

class InquirePsblOrderRequest(BaseModel):
    pdno: str  # 종목번호(6자리)* PDNO, ORD_UNPR 공란 입력 시, 매수수량 없이 매수금액만 조회됨
    ord_unpr: Optional[str] = ''   # 1주당 가격 * 시장가(ORD_DVSN:01)로 조회 시, 공란으로 입력 * PDNO, ORD_UNPR 공란 입력 시, 매수수량 없이 매수금액만 조회됨
    ord_dvsn :Optional[str] = '01'  # 특정 종목 전량매수 시 가능수량을 확인할 경우  00:지정가는 증거금율이 반영되지 않으므로  증거금율이 반영되는 01: 시장가로 조회 * 다만, 조건부지정가 등 특정 주문구분(ex.IOC)으로 주문 시 가능수량을 확인할 경우 주문 시와 동일한 주문구분(ex.IOC) 입력하여 가능수량 확인 * 종목별 매수가능수량 조회 없이 매수금액만 조회하고자 할 경우 임의값(00) 입력 00 : 지정가 01 : 시장가 02 : 조건부지정가 03 : 최유리지정가 04 : 최우선지정가 05 : 장전 시간외 06 : 장후 시간외 07 : 시간외 단일가 08 : 자기주식 09 : 자기주식S-Option 10 : 자기주식금전신탁 11 : IOC지정가 (즉시체결,잔량취소) 12 : FOK지정가 (즉시체결,전량취소) 13 : IOC시장가 (즉시체결,잔량취소) 14 : FOK시장가 (즉시체결,전량취소) 15 : IOC최유리 (즉시체결,잔량취소) 16 : FOK최유리 (즉시체결,전량취소) 51 : 장중대량 52 : 장중바스켓 62 : 장개시전 시간외대량 63 : 장개시전 시간외바스켓 67 : 장개시전 금전신탁자사주 69 : 장개시전 자기주식 72 : 시간외대량 77 : 시간외자사주신탁 79 : 시간외대량자기주식 80 : 바스켓
    cma_evlu_amt_icld_yn :Optional[str] = 'Y',  # CMA평가금액포함여부 Y : 포함 N : 포함하지 않음
    ovrs_icld_yn : Optional[str] = 'Y'  # 해외포함여부 Y : 포함 N : 포함하지 않음