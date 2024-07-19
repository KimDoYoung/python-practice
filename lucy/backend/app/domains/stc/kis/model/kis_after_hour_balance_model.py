# kis_after_hour_balance_model.py
"""
모듈 설명: 
    - 시간외호가잔량 모델
주요 기능:
    -   기능을 넣으시오

작성자: 김도영
작성일: 2024-07-18
버전: 1.0
"""
from typing import List
from backend.app.domains.stock_api_base_model import StockApiBaseModel

class AfterHourBalance_Request(StockApiBaseModel):
    fid_input_price_1: str  = "" # 입력 가격1 입력값 없을때 전체 (가격 ~)
    fid_cond_mrkt_div_code: str = "J" # 조건 시장 분류 코드 시장구분코드 (주식 J)
    fid_cond_scr_div_code: str = "20176"    # 조건 화면 분류 코드 Unique key( 20176 )
    fid_rank_sort_cls_code: str = "1" # 순위 정렬 구분 코드 1: 장전 시간외, 2: 장후 시간외, 3:매도잔량, 4:매수잔량
    fid_div_cls_code: str = "0"  # 분류 구분 코드 0 : 전체
    fid_input_iscd: str  = "0000"   # 입력 종목코드 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200
    fid_trgt_exls_cls_code: str = "0"   # 대상 제외 구분 코드 0 : 전체
    fid_trgt_cls_code: str = "0"     # 대상 구분 코드 0 : 전체
    fid_vol_cnt: str = ""   # 거래량 수 입력값 없을때 전체 (거래량 ~)
    fid_input_price_2: str = ""     # 입력 가격2 입력값 없을때 전체 (~ 가격)

class AfterHourBalanceItem(StockApiBaseModel):
    stck_shrn_iscd: str # 주식 단축 종목코드 
    data_rank: str # 데이터 순위 
    hts_kor_isnm: str # HTS 한글 종목명 
    stck_prpr: str # 주식 현재가 
    prdy_vrss: str # 전일 대비 
    prdy_vrss_sign: str # 전일 대비 부호 
    prdy_ctrt: str # 전일 대비율 
    ovtm_total_askp_rsqn: str # 시간외 총 매도호가 잔량 
    ovtm_total_bidp_rsqn: str # 시간외 총 매수호가 잔량 
    mkob_otcp_vol: str # 장개시전 시간외종가 거래량 
    mkfa_otcp_vol: str # 장종료후 시간외종가 거래량 

class AfterHourBalance_Response(StockApiBaseModel):
    rt_cd: str # 성공 실패 여부 
    msg_cd: str # 응답코드 
    msg1: str # 응답메세지 
    output:  List[AfterHourBalanceItem] = []