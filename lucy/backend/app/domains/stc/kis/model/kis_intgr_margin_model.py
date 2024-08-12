from typing import List, Optional
from backend.app.domains.stock_api_base_model import StockApiBaseModel

##############################################################################################
# [국내주식] 주문/계좌 > 주식통합증거금 현황
##############################################################################################

class IntgrMargin_Request(StockApiBaseModel):
    # CANO: str # 종합계좌번호 계좌번호 체계(8-2)의 앞 8자리
    # ACNT_PRDT_CD: str # 계좌상품코드 계좌번호 체계(8-2)의 뒤 2자리
    CMA_EVLU_AMT_ICLD_YN: str = 'N' # CMA평가금액포함여부 N 입력
    WCRC_FRCR_DVSN_CD: str = '02' # 원화외화구분코드 01(외화기준),02(원화기준)
    FWEX_CTRT_FRCR_DVSN_CD: str = '02' # 선도환계약외화구분코드 01(외화기준),02(원화기준)

class IntgrMarginItem(StockApiBaseModel):
    acmga_rt: str # 계좌증거금율 
    acmga_pct100_aptm_rson: str # 계좌증거금100퍼센트지정사유 
    stck_cash_objt_amt: str # 주식현금대상금액 
    stck_sbst_objt_amt: str # 주식대용대상금액 
    stck_evlu_objt_amt: str # 주식평가대상금액 
    stck_ruse_psbl_objt_amt: str # 주식재사용가능대상금액 
    stck_fund_rpch_chgs_objt_amt: str # 주식펀드환매대금대상금액 
    stck_fncg_rdpt_objt_atm: str # 주식융자상환금대상금액 
    bond_ruse_psbl_objt_amt: str # 채권재사용가능대상금액 
    stck_cash_use_amt: str # 주식현금사용금액 
    stck_sbst_use_amt: str # 주식대용사용금액 
    stck_evlu_use_amt: str # 주식평가사용금액 
    stck_ruse_psbl_amt_use_amt: str # 주식재사용가능금사용금액 
    stck_fund_rpch_chgs_use_amt: str # 주식펀드환매대금사용금액 
    stck_fncg_rdpt_amt_use_amt: str # 주식융자상환금사용금액 
    bond_ruse_psbl_amt_use_amt: str # 채권재사용가능금사용금액 
    stck_cash_ord_psbl_amt: str # 주식현금주문가능금액 
    stck_sbst_ord_psbl_amt: str # 주식대용주문가능금액 
    stck_evlu_ord_psbl_amt: str # 주식평가주문가능금액 
    stck_ruse_psbl_ord_psbl_amt: str # 주식재사용가능주문가능금액 
    stck_fund_rpch_ord_psbl_amt: str # 주식펀드환매주문가능금액 
    bond_ruse_psbl_ord_psbl_amt: str # 채권재사용가능주문가능금액 
    rcvb_amt: str # 미수금액 
    stck_loan_grta_ruse_psbl_amt: str # 주식대출보증금재사용가능금액 
    stck_cash20_max_ord_psbl_amt: str # 주식현금20최대주문가능금액 
    stck_cash30_max_ord_psbl_amt: str # 주식현금30최대주문가능금액 
    stck_cash40_max_ord_psbl_amt: str # 주식현금40최대주문가능금액 
    stck_cash50_max_ord_psbl_amt: str # 주식현금50최대주문가능금액 
    stck_cash60_max_ord_psbl_amt: str # 주식현금60최대주문가능금액 
    stck_cash100_max_ord_psbl_amt: str # 주식현금100최대주문가능금액 
    stck_rsip100_max_ord_psbl_amt: str # 주식재사용불가100최대주문가능 
    bond_max_ord_psbl_amt: str # 채권최대주문가능금액 
    stck_fncg45_max_ord_psbl_amt: str # 주식융자45최대주문가능금액 
    stck_fncg50_max_ord_psbl_amt: str # 주식융자50최대주문가능금액 
    stck_fncg60_max_ord_psbl_amt: str # 주식융자60최대주문가능금액 
    stck_fncg70_max_ord_psbl_amt: str # 주식융자70최대주문가능금액 
    stck_stln_max_ord_psbl_amt: str # 주식대주최대주문가능금액 
    lmt_amt: str # 한도금액 
    ovrs_stck_itgr_mgna_dvsn_name: str # 해외주식통합증거금구분명 
    usd_objt_amt: str # 미화대상금액 
    usd_use_amt: str # 미화사용금액 
    usd_ord_psbl_amt: str # 미화주문가능금액 
    hkd_objt_amt: str # 홍콩달러대상금액 
    hkd_use_amt: str # 홍콩달러사용금액 
    hkd_ord_psbl_amt: str # 홍콩달러주문가능금액 
    jpy_objt_amt: str # 엔화대상금액 
    jpy_use_amt: str # 엔화사용금액 
    jpy_ord_psbl_amt: str # 엔화주문가능금액 
    cny_objt_amt: str # 위안화대상금액 
    cny_use_amt: str # 위안화사용금액 
    cny_ord_psbl_amt: str # 위안화주문가능금액 
    usd_ruse_objt_amt: str # 미화재사용대상금액 
    usd_ruse_amt: str # 미화재사용금액 
    usd_ruse_ord_psbl_amt: str # 미화재사용주문가능금액 
    hkd_ruse_objt_amt: str # 홍콩달러재사용대상금액 
    hkd_ruse_amt: str # 홍콩달러재사용금액 
    hkd_ruse_ord_psbl_amt: str # 홍콩달러재사용주문가능금액 
    jpy_ruse_objt_amt: str # 엔화재사용대상금액 
    jpy_ruse_amt: str # 엔화재사용금액 
    jpy_ruse_ord_psbl_amt: str # 엔화재사용주문가능금액 
    cny_ruse_objt_amt: str # 위안화재사용대상금액 
    cny_ruse_amt: str # 위안화재사용금액 
    cny_ruse_ord_psbl_amt: str # 위안화재사용주문가능금액 
    usd_gnrl_ord_psbl_amt: str # 미화일반주문가능금액 
    usd_itgr_ord_psbl_amt: str # 미화통합주문가능금액 
    hkd_gnrl_ord_psbl_amt: str # 홍콩달러일반주문가능금액 
    hkd_itgr_ord_psbl_amt: str # 홍콩달러통합주문가능금액 
    jpy_gnrl_ord_psbl_amt: str # 엔화일반주문가능금액 
    jpy_itgr_ord_psbl_amt: str # 엔화통합주문가능금액 
    cny_gnrl_ord_psbl_amt: str # 위안화일반주문가능금액 
    cny_itgr_ord_psbl_amt: str # 위안화통합주문가능금액 
    stck_itgr_cash20_ord_psbl_amt: str # 주식통합현금20주문가능금액 
    stck_itgr_cash30_ord_psbl_amt: str # 주식통합현금30주문가능금액 
    stck_itgr_cash40_ord_psbl_amt: str # 주식통합현금40주문가능금액 
    stck_itgr_cash50_ord_psbl_amt: str # 주식통합현금50주문가능금액 
    stck_itgr_cash60_ord_psbl_amt: str # 주식통합현금60주문가능금액 
    stck_itgr_cash100_ord_psbl_amt: str # 주식통합현금100주문가능금액 
    stck_itgr_100_ord_psbl_amt: str # 주식통합100주문가능금액 
    stck_itgr_fncg45_ord_psbl_amt: str # 주식통합융자45주문가능금액 
    stck_itgr_fncg50_ord_psbl_amt: str # 주식통합융자50주문가능금액 
    stck_itgr_fncg60_ord_psbl_amt: str # 주식통합융자60주문가능금액 
    stck_itgr_fncg70_ord_psbl_amt: str # 주식통합융자70주문가능금액 
    stck_itgr_stln_ord_psbl_amt: str # 주식통합대주주문가능금액 
    bond_itgr_ord_psbl_amt: str # 채권통합주문가능금액 
    stck_cash_ovrs_use_amt: str # 주식현금해외사용금액 
    stck_sbst_ovrs_use_amt: str # 주식대용해외사용금액 
    stck_evlu_ovrs_use_amt: str # 주식평가해외사용금액 
    stck_re_use_amt_ovrs_use_amt: str # 주식재사용금액해외사용금액 
    stck_fund_rpch_ovrs_use_amt: str # 주식펀드환매해외사용금액 
    stck_fncg_rdpt_ovrs_use_amt: str # 주식융자상환해외사용금액 
    bond_re_use_ovrs_use_amt: str # 채권재사용해외사용금액 
    usd_oth_mket_use_amt: str # 미화타시장사용금액 
    jpy_oth_mket_use_amt: str # 엔화타시장사용금액 
    cny_oth_mket_use_amt: str # 위안화타시장사용금액 
    hkd_oth_mket_use_amt: str # 홍콩달러타시장사용금액 
    usd_re_use_oth_mket_use_amt: str # 미화재사용타시장사용금액 
    jpy_re_use_oth_mket_use_amt: str # 엔화재사용타시장사용금액 
    cny_re_use_oth_mket_use_amt: str # 위안화재사용타시장사용금액 
    hkd_re_use_oth_mket_use_amt: str # 홍콩달러재사용타시장사용금액 
    hgkg_cny_re_use_amt: str # 홍콩위안화재사용금액 
    
class IntgrMargin_Response(StockApiBaseModel):
    rt_cd: str # 성공 실패 여부 
    msg_cd: str # 응답코드 
    msg1: str # 응답메세지 
    output: Optional[IntgrMarginItem] = None 