from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class FieldMapping(BaseModel):
    Element: str
    한글명: str
    Type: str
    Required: str
    Length: int
    Description: str


KEY_MAPPING: List[FieldMapping] = [
    FieldMapping(Element="pdno", 한글명="상품번호", Type="String", Required="Y", Length=12, Description="종목번호(뒷 6자리)"),
    FieldMapping(Element="prdt_name", 한글명="상품명", Type="String", Required="Y", Length=60, Description="종목명"),
    FieldMapping(Element="trad_dvsn_name", 한글명="매매구분명", Type="String", Required="Y", Length=60, Description="매수매도구분"),
    FieldMapping(Element="bfdy_buy_qty", 한글명="전일매수수량", Type="String", Required="Y", Length=10, Description=""),
    FieldMapping(Element="bfdy_sll_qty", 한글명="전일매도수량", Type="String", Required="Y", Length=10, Description=""),
    FieldMapping(Element="thdt_buyqty", 한글명="금일매수수량", Type="String", Required="Y", Length=10, Description=""),
    FieldMapping(Element="thdt_sll_qty", 한글명="금일매도수량", Type="String", Required="Y", Length=10, Description=""),
    FieldMapping(Element="hldg_qty", 한글명="보유수량", Type="String", Required="Y", Length=19, Description=""),
    FieldMapping(Element="ord_psbl_qty", 한글명="주문가능수량", Type="String", Required="Y", Length=10, Description=""),
    FieldMapping(Element="pchs_avg_pric", 한글명="매입평균가격", Type="String", Required="Y", Length=22, Description="매입금액 / 보유수량"),
    FieldMapping(Element="pchs_amt", 한글명="매입금액", Type="String", Required="Y", Length=19, Description=""),
    FieldMapping(Element="prpr", 한글명="현재가", Type="String", Required="Y", Length=19, Description=""),
    FieldMapping(Element="evlu_amt", 한글명="평가금액", Type="String", Required="Y", Length=19, Description=""),
    FieldMapping(Element="evlu_pfls_amt", 한글명="평가손익금액", Type="String", Required="Y", Length=19, Description="평가금액 - 매입금액"),
    FieldMapping(Element="evlu_pfls_rt", 한글명="평가손익율", Type="String", Required="Y", Length=9, Description=""),
    FieldMapping(Element="evlu_erng_rt", 한글명="평가수익율", Type="String", Required="Y", Length=31, Description="미사용항목(0으로 출력)"),
    FieldMapping(Element="loan_dt", 한글명="대출일자", Type="String", Required="Y", Length=8, Description="INQR_DVSN(조회구분)을 01(대출일별)로 설정해야 값이 나옴"),
    FieldMapping(Element="loan_amt", 한글명="대출금액", Type="String", Required="Y", Length=19, Description=""),
    FieldMapping(Element="stln_slng_chgs", 한글명="대주매각대금", Type="String", Required="Y", Length=19, Description=""),
    FieldMapping(Element="expd_dt", 한글명="만기일자", Type="String", Required="Y", Length=8, Description=""),
    FieldMapping(Element="fltt_rt", 한글명="등락율", Type="String", Required="Y", Length=31, Description=""),
    FieldMapping(Element="bfdy_cprs_icdc", 한글명="전일대비증감", Type="String", Required="Y", Length=19, Description=""),
    FieldMapping(Element="item_mgna_rt_name", 한글명="종목증거금율명", Type="String", Required="Y", Length=20, Description=""),
    FieldMapping(Element="grta_rt_name", 한글명="보증금율명", Type="String", Required="Y", Length=20, Description=""),
    FieldMapping(Element="sbst_pric", 한글명="대용가격", Type="String", Required="Y", Length=19, Description="증권매매의 위탁보증금으로서 현금 대신에 사용되는 유가증권 가격"),
    FieldMapping(Element="stck_loan_unpr", 한글명="주식대출단가", Type="String", Required="Y", Length=22, Description=""),
    FieldMapping(Element="dnca_tot_amt", 한글명="예수금총금액", Type="String", Required="Y", Length=19, Description="예수금"),
    FieldMapping(Element="nxdy_excc_amt", 한글명="익일정산금액", Type="String", Required="Y", Length=19, Description="D+1 예수금"),
    FieldMapping(Element="prvs_rcdl_excc_amt", 한글명="가수도정산금액", Type="String", Required="Y", Length=19, Description="D+2 예수금"),
    FieldMapping(Element="cma_evlu_amt", 한글명="CMA평가금액", Type="String", Required="Y", Length=19, Description=""),
    FieldMapping(Element="bfdy_buy_amt", 한글명="전일매수금액", Type="String", Required="Y", Length=19, Description=""),
    FieldMapping(Element="thdt_buy_amt", 한글명="금일매수금액", Type="String", Required="Y", Length=19, Description=""),
    FieldMapping(Element="nxdy_auto_rdpt_amt", 한글명="익일자동상환금액", Type="String", Required="Y", Length=19, Description=""),
    FieldMapping(Element="bfdy_sll_amt", 한글명="전일매도금액", Type="String", Required="Y", Length=19, Description=""),
    FieldMapping(Element="thdt_sll_amt", 한글명="금일매도금액", Type="String", Required="Y", Length=19, Description=""),
    FieldMapping(Element="d2_auto_rdpt_amt", 한글명="D+2자동상환금액", Type="String", Required="Y", Length=19, Description=""),
    FieldMapping(Element="bfdy_tlex_amt", 한글명="전일제비용금액", Type="String", Required="Y", Length=19, Description=""),
    FieldMapping(Element="thdt_tlex_amt", 한글명="금일제비용금액", Type="String", Required="Y", Length=19, Description=""),
    FieldMapping(Element="tot_loan_amt", 한글명="총대출금액", Type="String", Required="Y", Length=19, Description=""),
    FieldMapping(Element="scts_evlu_amt", 한글명="유가평가금액", Type="String", Required="Y", Length=19, Description=""),
    FieldMapping(Element="tot_evlu_amt", 한글명="총평가금액", Type="String", Required="Y", Length=19, Description="유가증권 평가금액 합계금액 + D+2 예수금"),
    FieldMapping(Element="nass_amt", 한글명="순자산금액", Type="String", Required="Y", Length=19, Description=""),
    FieldMapping(Element="fncg_gld_auto_rdpt_yn", 한글명="융자금자동상환여부", Type="String", Required="Y", Length=1, Description="보유현금에 대한 융자금만 차감여부 신용융자 매수체결 시점에서는 융자비율을 매매대금 100%로 계산 하였다가 수도결제일에 보증금에 해당하는 금액을 고객의 현금으로 충당하여 융자금을 감소시키는 업무"),
    FieldMapping(Element="pchs_amt_smtl_amt", 한글명="매입금액합계금액", Type="String", Required="Y", Length=19, Description=""),
    FieldMapping(Element="evlu_amt_smtl_amt", 한글명="평가금액합계금액", Type="String", Required="Y", Length=19, Description="유가증권 평가금액 합계금액"),
    FieldMapping(Element="evlu_pfls_smtl_amt", 한글명="평가손익합계금액", Type="String", Required="Y", Length=19, Description=""),
    FieldMapping(Element="tot_stln_slng_chgs", 한글명="총대주매각대금", Type="String", Required="Y", Length=19, Description=""),
    FieldMapping(Element="bfdy_tot_asst_evlu_amt", 한글명="전일총자산평가금액", Type="String", Required="Y", Length=19, Description=""),
    FieldMapping(Element="asst_icdc_amt", 한글명="자산증감액", Type="String", Required="Y", Length=19, Description=""),
    FieldMapping(Element="asst_icdc_erng_rt", 한글명="자산증감수익율", Type="String", Required="Y", Length=31, Description="데이터 미제공"),
]



# 한글명을 요소로 실제 필드를 찾는 함수
def get_element_by_korean_name(korean_name: str) -> Optional[str]:
    for field in KEY_MAPPING:
        if field.한글명 == korean_name:
            return field.Element
    return None
