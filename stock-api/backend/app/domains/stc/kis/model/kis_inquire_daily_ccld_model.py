from typing import List, Optional
from pydantic import BaseModel, field_validator, validator

from backend.app.domains.stock_api_base_model import KisBaseModel
from pydantic import BaseModel

class InquireDailyCcldItem1(BaseModel):
    ord_dt: str  # 주문일자
    ord_gno_brno: str  # 주문채번지점번호
    odno: str  # 주문번호
    orgn_odno: str  # 원주문번호
    ord_dvsn_name: str  # 주문구분명
    sll_buy_dvsn_cd: str  # 매도매수구분코드
    sll_buy_dvsn_cd_name: str  # 매도매수구분코드명
    pdno: str  # 상품번호
    prdt_name: str  # 상품명
    ord_qty: str  # 주문수량
    ord_unpr: str  # 주문단가
    ord_tmd: str  # 주문시각
    tot_ccld_qty: str  # 총체결수량
    avg_prvs: str  # 평균가
    cncl_yn: str  # 취소여부
    tot_ccld_amt: str  # 총체결금액
    loan_dt: str  # 대출일자
    ord_dvsn_cd: str  # 주문구분코드
    cncl_cfrm_qty: str  # 취소확인수량
    rmn_qty: str  # 잔여수량
    rjct_qty: str  # 거부수량
    ccld_cndt_name: str  # 체결조건명
    infm_tmd: str  # 통보시각
    ctac_tlno: str  # 연락전화번호
    prdt_type_cd: str  # 상품유형코드
    excg_dvsn_cd: str  # 거래소구분코드


class InquireDailyCcldItem2(BaseModel):
    tot_ord_qty: str # 총주문수량 미체결주문수량 + 체결수량 (취소주문제외)
    tot_ccld_qty: str # 총체결수량 
    pchs_avg_pric: str # 매입평균가격 총체결금액 / 총체결수량
    tot_ccld_amt: str # 총체결금액 
    prsm_tlex_smtl: str # 추정제비용합계 제세 + 주문수수료 ※ 해당 값은 당일 데이터에 대해서만 제공됩니다.

class InquireDailyCcldDto(KisBaseModel):
    rt_cd: str # 성공 실패 여부 0 : 성공 0 이외의 값 : 실패
    msg_cd: str # 응답코드 응답코드
    msg1: str # 응답메세지 응답메세지
    ctx_area_fk100: str # 연속조회검색조건100 
    ctx_area_nk100: str # 연속조회키100 
    output1: Optional[List[InquireDailyCcldItem1]]
    output2: InquireDailyCcldItem2


class InquireDailyCcldRequest(BaseModel):
    inqr_strt_dt:str
    inqr_end_dt:str
    sll_buy_dvsn_cd: Optional[str] = "00" # 00 : 전체, 01 : 매도, 02 : 매수",  
    inqr_dvsn :  Optional[str] = "00" # 00 : 역순 01 : 정순",
    pdno: Optional[str] = "" # 종목번호 공란은 전체
    ccld_dvsn: Optional[str] = "" #00 : 전체 01 : 체결 02 : 미체결"
    inqr_dvsn_3:Optional[str] = "00" #00 : 전체 01 : 체결 02 : 미체결"
    CTX_AREA_FK100:Optional[str] = "" 
    CTX_AREA_NK100:Optional[str] = ""


    @field_validator('inqr_strt_dt', 'inqr_end_dt', mode='before')
    def remove_hyphens(cls, value):
        return value.replace('[^0-9]', '')
