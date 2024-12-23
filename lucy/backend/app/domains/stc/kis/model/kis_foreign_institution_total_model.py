# kis_foreign_institution_total_model.py
"""
모듈 설명: 
    - 국내기관외국인 매매종목가집계

작성자: 김도영
작성일: 2024-09-11
버전: 1.0
"""

from typing import List, Optional
from backend.app.domains.stock_api_base_model import StockApiBaseModel

class ForeignInstitutionTotal_Request(StockApiBaseModel):
    FID_COND_MRKT_DIV_CODE: str = 'V' # 시장 분류 코드 V(Default)
    FID_COND_SCR_DIV_CODE: str ='16449' # 조건 화면 분류 코드 16449(Default)
    FID_INPUT_ISCD: str = '0000' # 입력 종목코드 0000:전체, 0001:코스피, 1001:코스닥 ... 포탈 (FAQ : 종목정보 다운로드(국내) - 업종코드 참조)
    FID_DIV_CLS_CODE: str = '1' # 분류 구분 코드 0: 수량정열, 1: 금액정열
    FID_RANK_SORT_CLS_CODE: str = '0' # 순위 정렬 구분 코드 0: 순매수상위, 1: 순매도상위
    FID_ETC_CLS_CODE: str = '0' # 기타 구분 정렬 0:전체 1:외국인 2:기관계 3:기타


class ForeignInstitutionTotalItem(StockApiBaseModel):
    hts_kor_isnm: Optional[str] = None  # HTS 한글 종목명
    mksc_shrn_iscd: Optional[str] = None  # 유가증권 단축 종목코드
    ntby_qty: Optional[str] = None  # 순매수 수량
    stck_prpr: Optional[str] = None  # 주식 현재가
    prdy_vrss_sign: Optional[str] = None  # 전일 대비 부호
    prdy_vrss: Optional[str] = None  # 전일 대비
    prdy_ctrt: Optional[str] = None  # 전일 대비율
    acml_vol: Optional[str] = None  # 누적 거래량
    frgn_ntby_qty: Optional[str] = None  # 외국인 순매수 수량
    orgn_ntby_qty: Optional[str] = None  # 기관계 순매수 수량
    ivtr_ntby_qty: Optional[str] = None  # 투자신탁 순매수 수량
    bank_ntby_qty: Optional[str] = None  # 은행 순매수 수량
    insu_ntby_qty: Optional[str] = None  # 보험 순매수 수량
    mrbn_ntby_qty: Optional[str] = None  # 종금 순매수 수량
    fund_ntby_qty: Optional[str] = None  # 기금 순매수 수량
    etc_orgt_ntby_vol: Optional[str] = None  # 기타 단체 순매수 거래량
    etc_corp_ntby_vol: Optional[str] = None  # 기타 법인 순매수 거래량
    frgn_ntby_tr_pbmn: Optional[str] = None  # 외국인 순매수 거래 대금
    orgn_ntby_tr_pbmn: Optional[str] = None  # 기관계 순매수 거래 대금
    ivtr_ntby_tr_pbmn: Optional[str] = None  # 투자신탁 순매수 거래 대금
    bank_ntby_tr_pbmn: Optional[str] = None  # 은행 순매수 거래 대금
    insu_ntby_tr_pbmn: Optional[str] = None  # 보험 순매수 거래 대금
    mrbn_ntby_tr_pbmn: Optional[str] = None  # 종금 순매수 거래 대금
    fund_ntby_tr_pbmn: Optional[str] = None  # 기금 순매수 거래 대금
    etc_orgt_ntby_tr_pbmn: Optional[str] = None  # 기타 단체 순매수 거래 대금
    etc_corp_ntby_tr_pbmn: Optional[str] = None  # 기타 법인 순매수 거래 대금



class ForeignInstitutionTotal_Response(StockApiBaseModel):
    rt_cd: str # 성공 실패 여부 
    msg_cd: str # 응답코드 
    msg1: str # 응답메세지 
    output: List[ForeignInstitutionTotalItem]