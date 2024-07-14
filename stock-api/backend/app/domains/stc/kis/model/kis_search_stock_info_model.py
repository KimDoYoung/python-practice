from backend.app.domains.stock_api_base_model import StockApiBaseModel

from pydantic import BaseModel
from typing import Optional

class SearchStockInfoItem(BaseModel):
    pdno: Optional[str] = None  # 상품번호 
    prdt_type_cd: Optional[str] = None  # 상품유형코드 
    mket_id_cd: Optional[str] = None  # 시장ID코드 
    scty_grp_id_cd: Optional[str] = None  # 증권그룹ID코드 
    excg_dvsn_cd: Optional[str] = None  # 거래소구분코드 
    setl_mmdd: Optional[str] = None  # 결산월일 
    lstg_stqt: Optional[str] = None  # 상장주수 
    lstg_cptl_amt: Optional[str] = None  # 상장자본금액 
    cpta: Optional[str] = None  # 자본금 
    papr: Optional[str] = None  # 액면가 
    issu_pric: Optional[str] = None  # 발행가격 
    kospi200_item_yn: Optional[str] = None  # 코스피200종목여부 
    scts_mket_lstg_dt: Optional[str] = None  # 유가증권시장상장일자 
    scts_mket_lstg_abol_dt: Optional[str] = None  # 유가증권시장상장폐지일자 
    kosdaq_mket_lstg_dt: Optional[str] = None  # 코스닥시장상장일자 
    kosdaq_mket_lstg_abol_dt: Optional[str] = None  # 코스닥시장상장폐지일자 
    frbd_mket_lstg_dt: Optional[str] = None  # 프리보드시장상장일자 
    frbd_mket_lstg_abol_dt: Optional[str] = None  # 프리보드시장상장폐지일자 
    reits_kind_cd: Optional[str] = None  # 리츠종류코드 
    etf_dvsn_cd: Optional[str] = None  # ETF구분코드 
    oilf_fund_yn: Optional[str] = None  # 유전펀드여부 
    idx_bztp_lcls_cd: Optional[str] = None  # 지수업종대분류코드 
    idx_bztp_mcls_cd: Optional[str] = None  # 지수업종중분류코드 
    idx_bztp_scls_cd: Optional[str] = None  # 지수업종소분류코드 
    stck_kind_cd: Optional[str] = None  # 주식종류코드 
    mfnd_opng_dt: Optional[str] = None  # 뮤추얼펀드개시일자 
    mfnd_end_dt: Optional[str] = None  # 뮤추얼펀드종료일자 
    dpsi_erlm_cncl_dt: Optional[str] = None  # 예탁등록취소일자 
    etf_cu_qty: Optional[str] = None  # ETFCU수량 
    prdt_name: Optional[str] = None  # 상품명 
    prdt_name120: Optional[str] = None  # 상품명120 
    prdt_abrv_name: Optional[str] = None  # 상품약어명 
    std_pdno: Optional[str] = None  # 표준상품번호 
    prdt_eng_name: Optional[str] = None  # 상품영문명 
    prdt_eng_name120: Optional[str] = None  # 상품영문명120 
    prdt_eng_abrv_name: Optional[str] = None  # 상품영문약어명 
    dpsi_aptm_erlm_yn: Optional[str] = None  # 예탁지정등록여부 
    etf_txtn_type_cd: Optional[str] = None  # ETF과세유형코드 
    etf_type_cd: Optional[str] = None  # ETF유형코드 
    lstg_abol_dt: Optional[str] = None  # 상장폐지일자 
    nwst_odst_dvsn_cd: Optional[str] = None  # 신주구주구분코드 
    sbst_pric: Optional[str] = None  # 대용가격 
    thco_sbst_pric: Optional[str] = None  # 당사대용가격 
    thco_sbst_pric_chng_dt: Optional[str] = None  # 당사대용가격변경일자 
    tr_stop_yn: Optional[str] = None  # 거래정지여부 
    admn_item_yn: Optional[str] = None  # 관리종목여부 
    thdt_clpr: Optional[str] = None  # 당일종가 
    bfdy_clpr: Optional[str] = None  # 전일종가 
    clpr_chng_dt: Optional[str] = None  # 종가변경일자 
    std_idst_clsf_cd: Optional[str] = None  # 표준산업분류코드 
    std_idst_clsf_cd_name: Optional[str] = None  # 표준산업분류코드명 
    idx_bztp_lcls_cd_name: Optional[str] = None  # 지수업종대분류코드명 
    idx_bztp_mcls_cd_name: Optional[str] = None  # 지수업종중분류코드명 
    idx_bztp_scls_cd_name: Optional[str] = None  # 지수업종소분류코드명 
    ocr_no: Optional[str] = None  # OCR번호 
    crfd_item_yn: Optional[str] = None  # 크라우드펀딩종목여부 
    elec_scty_yn: Optional[str] = None  # 전자증권여부 
    issu_istt_cd: Optional[str] = None  # 발행기관코드 
    etf_chas_erng_rt_dbnb: Optional[str] = None  # ETF추적수익율배수 
    etf_etn_ivst_heed_item_yn: Optional[str] = None  # ETFETN투자유의종목여부 
    stln_int_rt_dvsn_cd: Optional[str] = None  # 대주이자율구분코드 
    frnr_psnl_lmt_rt: Optional[str] = None  # 외국인개인한도비율 
    lstg_rqsr_issu_istt_cd: Optional[str] = None  # 상장신청인발행기관코드 
    lstg_rqsr_item_cd: Optional[str] = None  # 상장신청인종목코드 
    trst_istt_issu_istt_cd: Optional[str] = None  # 신탁기관발행기관코드 


class SearchStockInfo_Response(StockApiBaseModel):
    rt_cd: str # 성공 실패 여부 
    msg_cd: str # 응답코드 
    msg1: str # 응답메세지 
    output: SearchStockInfoItem