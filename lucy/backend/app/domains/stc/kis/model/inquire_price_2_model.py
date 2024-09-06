# 주식현재가 시세2
from backend.app.domains.stock_api_base_model import StockApiBaseModel
from typing import Optional

class InquirePrice2_Request(StockApiBaseModel):
    FID_COND_MRKT_DIV_CODE: str = 'J' # FID 조건 시장 분류 코드 J : 주식, ETF, ETN
    FID_INPUT_ISCD: str # FID 입력 종목코드 000660

class InquirePrice2Item(StockApiBaseModel):
    rprs_mrkt_kor_name: Optional[str] = None  # 대표 시장 한글 명 
    new_hgpr_lwpr_cls_code: Optional[str] = None  # 신 고가 저가 구분 코드 특정 경우에만 데이터 출력
    mxpr_llam_cls_code: Optional[str] = None  # 상하한가 구분 코드 특정 경우에만 데이터 출력
    crdt_able_yn: Optional[str] = None  # 신용 가능 여부 
    stck_mxpr: Optional[str] = None  # 주식 상한가 
    elw_pblc_yn: Optional[str] = None  # ELW 발행 여부 
    prdy_clpr_vrss_oprc_rate: Optional[str] = None  # 전일 종가 대비 시가2 비율 
    crdt_rate: Optional[str] = None  # 신용 비율 
    marg_rate: Optional[str] = None  # 증거금 비율 
    lwpr_vrss_prpr: Optional[str] = None  # 최저가 대비 현재가 
    lwpr_vrss_prpr_sign: Optional[str] = None  # 최저가 대비 현재가 부호 
    prdy_clpr_vrss_lwpr_rate: Optional[str] = None  # 전일 종가 대비 최저가 비율 
    stck_lwpr: Optional[str] = None  # 주식 최저가 
    hgpr_vrss_prpr: Optional[str] = None  # 최고가 대비 현재가 
    hgpr_vrss_prpr_sign: Optional[str] = None  # 최고가 대비 현재가 부호 
    prdy_clpr_vrss_hgpr_rate: Optional[str] = None  # 전일 종가 대비 최고가 비율 
    stck_hgpr: Optional[str] = None  # 주식 최고가 
    oprc_vrss_prpr: Optional[str] = None  # 시가2 대비 현재가 
    oprc_vrss_prpr_sign: Optional[str] = None  # 시가2 대비 현재가 부호 
    mang_issu_yn: Optional[str] = None  # 관리 종목 여부 
    divi_app_cls_code: Optional[str] = None  # 동시호가배분처리코드
    short_over_yn: Optional[str] = None  # 단기과열여부 
    mrkt_warn_cls_code: Optional[str] = None  # 시장경고코드 
    invt_caful_yn: Optional[str] = None  # 투자유의여부 
    stange_runup_yn: Optional[str] = None  # 이상급등여부 
    ssts_hot_yn: Optional[str] = None  # 공매도과열 여부 
    low_current_yn: Optional[str] = None  # 저유동성 종목 여부 
    vi_cls_code: Optional[str] = None  # VI적용구분코드 
    short_over_cls_code: Optional[str] = None  # 단기과열구분코드 
    stck_llam: Optional[str] = None  # 주식 하한가 
    new_lstn_cls_name: Optional[str] = None  # 신규 상장 구분 명 
    vlnt_deal_cls_name: Optional[str] = None  # 임의 매매 구분 명 
    flng_cls_name: Optional[str] = None  # 락 구분 이름 
    revl_issu_reas_name: Optional[str] = None  # 재평가 종목 사유 명 
    mrkt_warn_cls_name: Optional[str] = None  # 시장 경고 구분 명 
    stck_sdpr: Optional[str] = None  # 주식 기준가 
    bstp_cls_code: Optional[str] = None  # 업종 구분 코드 
    stck_prdy_clpr: Optional[str] = None  # 주식 전일 종가 
    insn_pbnt_yn: Optional[str] = None  # 불성실 공시 여부 
    fcam_mod_cls_name: Optional[str] = None  # 액면가 변경 구분 명 
    stck_prpr: Optional[str] = None  # 주식 현재가 
    prdy_vrss: Optional[str] = None  # 전일 대비 
    prdy_vrss_sign: Optional[str] = None  # 전일 대비 부호 
    prdy_ctrt: Optional[str] = None  # 전일 대비율 
    acml_tr_pbmn: Optional[str] = None  # 누적 거래 대금 
    acml_vol: Optional[str] = None  # 누적 거래량 
    prdy_vrss_vol_rate: Optional[str] = None  # 전일 대비 거래량 비율 
    bstp_kor_isnm: Optional[str] = None  # 업종 한글 종목명 
    sltr_yn: Optional[str] = None  # 정리매매 여부 
    trht_yn: Optional[str] = None  # 거래정지 여부 
    oprc_rang_cont_yn: Optional[str] = None  # 시가 범위 연장 여부 
    vlnt_fin_cls_code: Optional[str] = None  # 임의 종료 구분 코드 
    stck_oprc: Optional[str] = None  # 주식 시가2 
    prdy_vol: Optional[str] = None  # 전일 거래량


class InquirePrice2_Response(StockApiBaseModel):
    rt_cd: str # 성공 실패 여부 
    msg_cd: str # 응답코드 
    msg1: str # 응답메세지 
    output: InquirePrice2Item