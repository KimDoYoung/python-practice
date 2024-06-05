from typing import List, Optional

from backend.app.domains.stc.kis.kis_base_model import KisBaseModel

class InquireBalanceItem1(KisBaseModel):
    pdno: str
    prdt_name: str
    trad_dvsn_name: str
    bfdy_buy_qty: str
    bfdy_sll_qty: str
    thdt_buyqty: str
    thdt_sll_qty: str
    hldg_qty: str
    ord_psbl_qty: str
    pchs_avg_pric: str
    pchs_amt: str
    prpr: str
    evlu_amt: str
    evlu_pfls_amt: str
    evlu_pfls_rt: str
    evlu_erng_rt: str
    loan_dt: Optional[str] = None
    loan_amt: str
    stln_slng_chgs: str
    expd_dt: Optional[str] = None
    fltt_rt: str
    bfdy_cprs_icdc: str
    item_mgna_rt_name: Optional[str] = None
    grta_rt_name: Optional[str] = None
    sbst_pric: str
    stck_loan_unpr: str

class InquireBalanceItem2(KisBaseModel):
    dnca_tot_amt: str
    nxdy_excc_amt: str
    prvs_rcdl_excc_amt: str
    cma_evlu_amt: str
    bfdy_buy_amt: str
    thdt_buy_amt: str
    nxdy_auto_rdpt_amt: str
    bfdy_sll_amt: str
    thdt_sll_amt: str
    d2_auto_rdpt_amt: str
    bfdy_tlex_amt: str
    thdt_tlex_amt: str
    tot_loan_amt: str
    scts_evlu_amt: str
    tot_evlu_amt: str
    nass_amt: str
    fncg_gld_auto_rdpt_yn: Optional[str] = None
    pchs_amt_smtl_amt: str
    evlu_amt_smtl_amt: str
    evlu_pfls_smtl_amt: str
    tot_stln_slng_chgs: str
    bfdy_tot_asst_evlu_amt: str
    asst_icdc_amt: str
    asst_icdc_erng_rt: str

class KisInquireBalance(KisBaseModel):
    rt_cd: str
    msg_cd: str
    msg1: str
    ctx_area_fk100: str
    ctx_area_nk100: str
    output1: List[InquireBalanceItem1]
    output2: List[InquireBalanceItem2]
