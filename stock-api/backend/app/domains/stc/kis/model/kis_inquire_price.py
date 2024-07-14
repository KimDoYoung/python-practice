# kis_inquire_price.py
"""
모듈 설명: 
    - KIS 현재가  응답 객체

주요 기능:

작성자: 김도영
작성일: 2024-07-12
버전: 1.0
"""
from typing import Optional
from backend.app.domains.stock_api_base_model import StockApiBaseModel

class InquirePrice(StockApiBaseModel):
    iscd_stat_cls_code: Optional[str] = None  # 종목 상태 구분 코드
    marg_rate: Optional[str] = None  # 증거금 비율
    rprs_mrkt_kor_name: Optional[str] = None  # 대표 시장 한글 명
    new_hgpr_lwpr_cls_code: Optional[str] = None  # 신 고가 저가 구분 코드
    bstp_kor_isnm: Optional[str] = None  # 업종 한글 종목명
    temp_stop_yn: Optional[str] = None  # 임시 정지 여부
    oprc_rang_cont_yn: Optional[str] = None  # 시가 범위 연장 여부
    clpr_rang_cont_yn: Optional[str] = None  # 종가 범위 연장 여부
    crdt_able_yn: Optional[str] = None  # 신용 가능 여부
    grmn_rate_cls_code: Optional[str] = None  # 보증금 비율 구분 코드
    elw_pblc_yn: Optional[str] = None  # ELW 발행 여부
    stck_prpr: Optional[str] = None  # 주식 현재가
    prdy_vrss: Optional[str] = None  # 전일 대비
    prdy_vrss_sign: Optional[str] = None  # 전일 대비 부호
    prdy_ctrt: Optional[str] = None  # 전일 대비율
    acml_tr_pbmn: Optional[str] = None  # 누적 거래 대금
    acml_vol: Optional[str] = None  # 누적 거래량
    prdy_vrss_vol_rate: Optional[str] = None  # 전일 대비 거래량 비율
    stck_oprc: Optional[str] = None  # 주식 시가
    stck_hgpr: Optional[str] = None  # 주식 최고가
    stck_lwpr: Optional[str] = None  # 주식 최저가
    stck_mxpr: Optional[str] = None  # 주식 상한가
    stck_llam: Optional[str] = None  # 주식 하한가
    stck_sdpr: Optional[str] = None  # 주식 기준가
    wghn_avrg_stck_prc: Optional[str] = None  # 가중 평균 주식 가격
    hts_frgn_ehrt: Optional[str] = None  # HTS 외국인 소진율
    frgn_ntby_qty: Optional[str] = None  # 외국인 순매수 수량
    pgtr_ntby_qty: Optional[str] = None  # 프로그램매매 순매수 수량
    pvt_scnd_dmrs_prc: Optional[str] = None  # 피벗 2차 디저항 가격
    pvt_frst_dmrs_prc: Optional[str] = None  # 피벗 1차 디저항 가격
    pvt_pont_val: Optional[str] = None  # 피벗 포인트 값
    pvt_frst_dmsp_prc: Optional[str] = None  # 피벗 1차 디지지 가격
    pvt_scnd_dmsp_prc: Optional[str] = None  # 피벗 2차 디지지 가격
    dmrs_val: Optional[str] = None  # 디저항 값
    dmsp_val: Optional[str] = None  # 디지지 값
    cpfn: Optional[str] = None  # 자본금
    rstc_wdth_prc: Optional[str] = None  # 제한 폭 가격
    stck_fcam: Optional[str] = None  # 주식 액면가
    stck_sspr: Optional[str] = None  # 주식 대용가
    aspr_unit: Optional[str] = None  # 호가단위
    hts_deal_qty_unit_val: Optional[str] = None  # HTS 매매 수량 단위 값
    lstn_stcn: Optional[str] = None  # 상장 주수
    hts_avls: Optional[str] = None  # HTS 시가총액
    per: Optional[str] = None  # PER
    pbr: Optional[str] = None  # PBR
    stac_month: Optional[str] = None  # 결산 월
    vol_tnrt: Optional[str] = None  # 거래량 회전율
    eps: Optional[str] = None  # EPS
    bps: Optional[str] = None  # BPS
    d250_hgpr: Optional[str] = None  # 250일 최고가
    d250_hgpr_date: Optional[str] = None  # 250일 최고가 일자
    d250_hgpr_vrss_prpr_rate: Optional[str] = None  # 250일 최고가 대비 현재가 비율
    d250_lwpr: Optional[str] = None  # 250일 최저가
    d250_lwpr_date: Optional[str] = None  # 250일 최저가 일자
    d250_lwpr_vrss_prpr_rate: Optional[str] = None  # 250일 최저가 대비 현재가 비율
    stck_dryy_hgpr: Optional[str] = None  # 주식 연중 최고가
    dryy_hgpr_vrss_prpr_rate: Optional[str] = None  # 연중 최고가 대비 현재가 비율
    dryy_hgpr_date: Optional[str] = None  # 연중 최고가 일자
    stck_dryy_lwpr: Optional[str] = None  # 주식 연중 최저가
    dryy_lwpr_vrss_prpr_rate: Optional[str] = None  # 연중 최저가 대비 현재가 비율
    dryy_lwpr_date: Optional[str] = None  # 연중 최저가 일자
    w52_hgpr: Optional[str] = None  # 52주일 최고가
    w52_hgpr_vrss_prpr_ctrt: Optional[str] = None  # 52주일 최고가 대비 현재가 대비
    w52_hgpr_date: Optional[str] = None  # 52주일 최고가 일자
    w52_lwpr: Optional[str] = None  # 52주일 최저가
    w52_lwpr_vrss_prpr_ctrt: Optional[str] = None  # 52주일 최저가 대비 현재가 대비
    w52_lwpr_date: Optional[str] = None  # 52주일 최저가 일자
    whol_loan_rmnd_rate: Optional[str] = None  # 전체 융자 잔고 비율
    ssts_yn: Optional[str] = None  # 공매도가능여부
    stck_shrn_iscd: Optional[str] = None  # 주식 단축 종목코드
    fcam_cnnm: Optional[str] = None  # 액면가 통화명
    cpfn_cnnm: Optional[str] = None  # 자본금 통화명
    apprch_rate: Optional[str] = None  # 접근도
    frgn_hldn_qty: Optional[str] = None  # 외국인 보유 수량
    vi_cls_code: Optional[str] = None  # VI적용구분코드
    ovtm_vi_cls_code: Optional[str] = None  # 시간외단일가VI적용구분코드
    last_ssts_cntg_qty: Optional[str] = None  # 최종 공매도 체결 수량
    invt_caful_yn: Optional[str] = None  # 투자유의여부
    mrkt_warn_cls_code: Optional[str] = None  # 시장경고코드
    short_over_yn: Optional[str] = None  # 단기과열여부
    sltr_yn: Optional[str] = None  # 정리매매여부
    
class InquirePrice_Response(StockApiBaseModel):
    rt_cd: str # 성공 실패 여부 0 : 성공 0 이외의 값 : 실패
    msg_cd: str # 응답코드 응답코드
    msg1: str # 응답메세지 응답메세지
    output: InquirePrice
