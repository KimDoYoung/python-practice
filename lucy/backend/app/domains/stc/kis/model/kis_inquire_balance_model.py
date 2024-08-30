from typing import List, Optional

from backend.app.domains.stock_api_base_model import StockApiBaseModel

class InquireBalanceItem1(StockApiBaseModel):
    pdno: str  # 상품번호
    prdt_name: str  # 상품명
    trad_dvsn_name: str  # 매매구분명
    bfdy_buy_qty: str  # 전일매수수량
    bfdy_sll_qty: str  # 전일매도수량
    thdt_buyqty: str  # 금일매수수량
    thdt_sll_qty: str  # 금일매도수량
    hldg_qty: str  # 보유수량
    ord_psbl_qty: str  # 주문가능수량
    pchs_avg_pric: str  # 매입평균가격
    pchs_amt: str  # 매입금액
    prpr: str  # 현재가
    evlu_amt: str  # 평가금액
    evlu_pfls_amt: str  # 평가손익금액
    evlu_pfls_rt: str  # 평가손익율
    evlu_erng_rt: str  # 평가수익율
    loan_dt: Optional[str] = None  # 대출일자
    loan_amt: str  # 대출금액
    stln_slng_chgs: str  # 대주매각대금
    expd_dt: Optional[str] = None  # 만기일자
    fltt_rt: str  # 등락율
    bfdy_cprs_icdc: str  # 전일대비증감
    item_mgna_rt_name: Optional[str] = None  # 종목증거금율명
    grta_rt_name: Optional[str] = None  # 보증금율명
    sbst_pric: str  # 대용가격
    stck_loan_unpr: str  # 주식대출단가

class InquireBalanceItem2(StockApiBaseModel):
    dnca_tot_amt: str  # 예수금총금액
    nxdy_excc_amt: str  # 익일정산금액
    prvs_rcdl_excc_amt: str  # 가수도정산금액
    cma_evlu_amt: str  # CMA평가금액
    bfdy_buy_amt: str  # 전일매수금액
    thdt_buy_amt: str  # 금일매수금액
    nxdy_auto_rdpt_amt: str  # 익일자동상환금액
    bfdy_sll_amt: str  # 전일매도금액
    thdt_sll_amt: str  # 금일매도금액
    d2_auto_rdpt_amt: str  # D+2자동상환금액
    bfdy_tlex_amt: str  # 전일제비용금액
    thdt_tlex_amt: str  # 금일제비용금액
    tot_loan_amt: str  # 총대출금액
    scts_evlu_amt: str  # 유가평가금액
    tot_evlu_amt: str  # 총평가금액
    nass_amt: str  # 순자산금액
    fncg_gld_auto_rdpt_yn: Optional[str] = None  # 융자금자동상환여부
    pchs_amt_smtl_amt: str  # 매입금액합계금액
    evlu_amt_smtl_amt: str  # 평가금액합계금액
    evlu_pfls_smtl_amt: str  # 평가손익합계금액
    tot_stln_slng_chgs: str  # 총대주매각대금
    bfdy_tot_asst_evlu_amt: str  # 전일총자산평가금액
    asst_icdc_amt: str  # 자산증감액
    asst_icdc_erng_rt: str  # 자산증감수익율

class KisInquireBalance_Response(StockApiBaseModel):
    rt_cd: str  # 성공 실패 여부
    msg_cd: str  # 응답코드
    msg1: str  # 응답메세지
    ctx_area_fk100: str  # 연속조회검색조건100
    ctx_area_nk100: str  # 연속조회키100
    output1: List[InquireBalanceItem1]  # 응답상세1
    output2: List[InquireBalanceItem2]  # 응답상세2


# class InquireBalanceItem1(StockApiBaseModel):
#     pdno: str
#     prdt_name: str
#     trad_dvsn_name: str
#     bfdy_buy_qty: str
#     bfdy_sll_qty: str
#     thdt_buyqty: str
#     thdt_sll_qty: str
#     hldg_qty: str
#     ord_psbl_qty: str
#     pchs_avg_pric: str
#     pchs_amt: str
#     prpr: str
#     evlu_amt: str
#     evlu_pfls_amt: str
#     evlu_pfls_rt: str
#     evlu_erng_rt: str
#     loan_dt: Optional[str] = None
#     loan_amt: str
#     stln_slng_chgs: str
#     expd_dt: Optional[str] = None
#     fltt_rt: str
#     bfdy_cprs_icdc: str
#     item_mgna_rt_name: Optional[str] = None
#     grta_rt_name: Optional[str] = None
#     sbst_pric: str
#     stck_loan_unpr: str

# class InquireBalanceItem2(StockApiBaseModel):
#     dnca_tot_amt: str
#     nxdy_excc_amt: str
#     prvs_rcdl_excc_amt: str
#     cma_evlu_amt: str
#     bfdy_buy_amt: str
#     thdt_buy_amt: str
#     nxdy_auto_rdpt_amt: str
#     bfdy_sll_amt: str
#     thdt_sll_amt: str
#     d2_auto_rdpt_amt: str
#     bfdy_tlex_amt: str
#     thdt_tlex_amt: str
#     tot_loan_amt: str
#     scts_evlu_amt: str
#     tot_evlu_amt: str
#     nass_amt: str
#     fncg_gld_auto_rdpt_yn: Optional[str] = None
#     pchs_amt_smtl_amt: str
#     evlu_amt_smtl_amt: str
#     evlu_pfls_smtl_amt: str
#     tot_stln_slng_chgs: str
#     bfdy_tot_asst_evlu_amt: str
#     asst_icdc_amt: str
#     asst_icdc_erng_rt: str

# class KisInquireBalance_Response(StockApiBaseModel):
#     rt_cd: str
#     msg_cd: str
#     msg1: str
#     ctx_area_fk100: str
#     ctx_area_nk100: str
#     output1: List[InquireBalanceItem1]
#     output2: List[InquireBalanceItem2]
