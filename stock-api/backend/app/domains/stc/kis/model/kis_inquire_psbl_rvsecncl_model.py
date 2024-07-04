from typing import List


from backend.app.domains.stock_api_base_model import KisBaseModel


##############################################################################################
# [국내주식] 주문/계좌 > 주식정정취소가능주문조회[v1_국내주식-004]
##############################################################################################

class InquirePsblRvsecnclItem(KisBaseModel):
    ord_gno_brno: str # 주문채번지점번호 주문시 한국투자증권 시스템에서 지정된 영업점코드
    odno: str # 주문번호 주문시 한국투자증권 시스템에서 채번된 주문번호
    orgn_odno: str # 원주문번호 정정/취소주문 인경우 원주문번호
    ord_dvsn_name: str # 주문구분명 
    pdno: str # 상품번호 종목번호(뒤 6자리만 해당)
    prdt_name: str # 상품명 종목명
    rvse_cncl_dvsn_name: str # 정정취소구분명 정정 또는 취소 여부 표시
    ord_qty: str # 주문수량 주문수량
    ord_unpr: str # 주문단가 1주당 주문가격
    ord_tmd: str # 주문시각 주문시각(시분초HHMMSS)
    tot_ccld_qty: str # 총체결수량 주문 수량 중 체결된 수량
    tot_ccld_amt: str # 총체결금액 주문금액 중 체결금액
    psbl_qty: str # 가능수량 정정/취소 주문 가능 수량
    sll_buy_dvsn_cd: str # 매도매수구분코드 01 : 매도 02 : 매수
    ord_dvsn_cd: str # 주문구분코드 00 : 지정가 01 : 시장가 02 : 조건부지정가 03 : 최유리지정가 04 : 최우선지정가 05 : 장전 시간외 06 : 장후 시간외 07 : 시간외 단일가 08 : 자기주식 09 : 자기주식S-Option 10 : 자기주식금전신탁 11 : IOC지정가 (즉시체결,잔량취소) 12 : FOK지정가 (즉시체결,전량취소) 13 : IOC시장가 (즉시체결,잔량취소) 14 : FOK시장가 (즉시체결,전량취소) 15 : IOC최유리 (즉시체결,잔량취소) 16 : FOK최유리 (즉시체결,전량취소) 51 : 장중대량
    mgco_aptm_odno: str # 운용사지정주문번호 주문 번호 (운용사 통한 주문)


class InquirePsblRvsecnclDto(KisBaseModel):
    rt_cd: str # 성공 실패 여부 0 : 성공 0 이외의 값 : 실패
    msg_cd: str # 응답코드 응답코드
    msg1: str # 응답메세지 응답메세지
    ctx_area_fk100: str # 연속조회검색조건100 
    ctx_area_nk100: str # 연속조회키100 
    output: List[InquirePsblRvsecnclItem]