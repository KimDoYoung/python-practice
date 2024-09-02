from typing import List, Optional
from backend.app.domains.stock_api_base_model import StockApiBaseModel

class IntstockMultprice_Request(StockApiBaseModel):
    FID_COND_MRKT_DIV_CODE_1: str # 조건 시장 분류 코드1 그룹별종목조회 결과 fid_mrkt_cls_code(시장구분) 1 입력 ex) J
    FID_INPUT_ISCD_1: str # 입력 종목코드1 그룹별종목조회 결과 jong_code(종목코드) 1 입력 ex) 005930
    FID_COND_MRKT_DIV_CODE_2: str # 조건 시장 분류 코드2 nan
    FID_INPUT_ISCD_2: str # 입력 종목코드2 nan
    FID_COND_MRKT_DIV_CODE_3: str # 조건 시장 분류 코드3 nan
    FID_INPUT_ISCD_3: str # 입력 종목코드3 nan
    FID_COND_MRKT_DIV_CODE_4: str # 조건 시장 분류 코드4 nan
    FID_INPUT_ISCD_4: str # 입력 종목코드4 nan
    FID_COND_MRKT_DIV_CODE_5: str # 조건 시장 분류 코드5 nan
    FID_INPUT_ISCD_5: str # 입력 종목코드5 nan
    FID_COND_MRKT_DIV_CODE_6: str # 조건 시장 분류 코드6 nan
    FID_INPUT_ISCD_6: str # 입력 종목코드6 nan
    FID_COND_MRKT_DIV_CODE_7: str # 조건 시장 분류 코드7 nan
    FID_INPUT_ISCD_7: str # 입력 종목코드7 nan
    FID_COND_MRKT_DIV_CODE_8: str # 조건 시장 분류 코드8 nan
    FID_INPUT_ISCD_8: str # 입력 종목코드8 nan
    FID_COND_MRKT_DIV_CODE_9: str # 조건 시장 분류 코드9 nan
    FID_INPUT_ISCD_9: str # 입력 종목코드9 nan
    FID_COND_MRKT_DIV_CODE_10: str # 조건 시장 분류 코드10 nan
    FID_INPUT_ISCD_10: str # 입력 종목코드10 nan
    FID_COND_MRKT_DIV_CODE_11: str # 조건 시장 분류 코드11 nan
    FID_INPUT_ISCD_11: str # 입력 종목코드11 nan
    FID_COND_MRKT_DIV_CODE_12: str # 조건 시장 분류 코드12 nan
    FID_INPUT_ISCD_12: str # 입력 종목코드12 nan
    FID_COND_MRKT_DIV_CODE_13: str # 조건 시장 분류 코드13 nan
    FID_INPUT_ISCD_13: str # 입력 종목코드13 nan
    FID_COND_MRKT_DIV_CODE_14: str # 조건 시장 분류 코드14 nan
    FID_INPUT_ISCD_14: str # 입력 종목코드14 nan
    FID_COND_MRKT_DIV_CODE_15: str # 조건 시장 분류 코드15 nan
    FID_INPUT_ISCD_15: str # 입력 종목코드15 nan
    FID_COND_MRKT_DIV_CODE_16: str # 조건 시장 분류 코드16 nan
    FID_INPUT_ISCD_16: str # 입력 종목코드16 nan
    FID_COND_MRKT_DIV_CODE_17: str # 조건 시장 분류 코드17 nan
    FID_INPUT_ISCD_17: str # 입력 종목코드17 nan
    FID_COND_MRKT_DIV_CODE_18: str # 조건 시장 분류 코드18 nan
    FID_INPUT_ISCD_18: str # 입력 종목코드18 nan
    FID_COND_MRKT_DIV_CODE_19: str # 조건 시장 분류 코드19 nan
    FID_INPUT_ISCD_19: str # 입력 종목코드19 nan
    FID_COND_MRKT_DIV_CODE_20: str # 조건 시장 분류 코드20 nan
    FID_INPUT_ISCD_20: str # 입력 종목코드20 nan
    FID_COND_MRKT_DIV_CODE_21: str # 조건 시장 분류 코드21 nan
    FID_INPUT_ISCD_21: str # 입력 종목코드21 nan
    FID_COND_MRKT_DIV_CODE_22: str # 조건 시장 분류 코드22 nan
    FID_INPUT_ISCD_22: str # 입력 종목코드22 nan
    FID_COND_MRKT_DIV_CODE_23: str # 조건 시장 분류 코드23 nan
    FID_INPUT_ISCD_23: str # 입력 종목코드23 nan
    FID_COND_MRKT_DIV_CODE_24: str # 조건 시장 분류 코드24 nan
    FID_INPUT_ISCD_24: str # 입력 종목코드24 nan
    FID_COND_MRKT_DIV_CODE_25: str # 조건 시장 분류 코드25 nan
    FID_INPUT_ISCD_25: str # 입력 종목코드25 nan
    FID_COND_MRKT_DIV_CODE_26: str # 조건 시장 분류 코드26 nan
    FID_INPUT_ISCD_26: str # 입력 종목코드26 nan
    FID_COND_MRKT_DIV_CODE_27: str # 조건 시장 분류 코드27 nan
    FID_INPUT_ISCD_27: str # 입력 종목코드27 nan
    FID_COND_MRKT_DIV_CODE_28: str # 조건 시장 분류 코드28 nan
    FID_INPUT_ISCD_28: str # 입력 종목코드28 nan
    FID_COND_MRKT_DIV_CODE_29: str # 조건 시장 분류 코드29 nan
    FID_INPUT_ISCD_29: str # 입력 종목코드29 nan
    FID_COND_MRKT_DIV_CODE_30: str # 조건 시장 분류 코드30 nan
    FID_INPUT_ISCD_30: str # 입력 종목코드30 nan

class IntstockMultpriceItem(StockApiBaseModel):
    kospi_kosdaq_cls_name: str # 코스피 코스닥 구분 명 
    mrkt_trtm_cls_name: str # 시장 조치 구분 명 
    hour_cls_code: str # 시간 구분 코드 
    inter_shrn_iscd: str # 관심 단축 종목코드 
    inter_kor_isnm: str # 관심 한글 종목명 
    inter2_prpr: str # 관심2 현재가 
    inter2_prdy_vrss: str # 관심2 전일 대비 
    prdy_vrss_sign: str # 전일 대비 부호 
    prdy_ctrt: str # 전일 대비율 
    acml_vol: str # 누적 거래량 
    inter2_oprc: str # 관심2 시가 
    inter2_hgpr: str # 관심2 고가 
    inter2_lwpr: str # 관심2 저가 
    inter2_llam: str # 관심2 하한가 
    inter2_mxpr: str # 관심2 상한가 
    inter2_askp: str # 관심2 매도호가 
    inter2_bidp: str # 관심2 매수호가 
    seln_rsqn: str # 매도 잔량 
    shnu_rsqn: str # 매수2 잔량 
    total_askp_rsqn: str # 총 매도호가 잔량 
    total_bidp_rsqn: str # 총 매수호가 잔량 
    acml_tr_pbmn: str # 누적 거래 대금 
    inter2_prdy_clpr: str # 관심2 전일 종가 
    oprc_vrss_hgpr_rate: str # 시가 대비 최고가 비율 
    intr_antc_cntg_vrss: str # 관심 예상 체결 대비 
    intr_antc_cntg_vrss_sign: str # 관심 예상 체결 대비 부호 
    intr_antc_cntg_prdy_ctrt: str # 관심 예상 체결 전일 대비율 
    intr_antc_vol: str # 관심 예상 거래량 
    inter2_sdpr: str # 관심2 기준가 

class IntstockMultprice_Response(StockApiBaseModel):
    rt_cd: str # 성공 실패 여부 
    msg_cd: str # 응답코드 
    msg1: str # 응답메세지 
    output: Optional[List[IntstockMultpriceItem]] = None
