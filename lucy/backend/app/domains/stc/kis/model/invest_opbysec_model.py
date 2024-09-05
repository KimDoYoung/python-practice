# 국내주식 증권사별 투자의견 
from typing import List
from backend.app.domains.stock_api_base_model import StockApiBaseModel


class InvestOpbysec_Request(StockApiBaseModel):
    FID_COND_MRKT_DIV_CODE: str ='J' # 조건시장분류코드 J(시장 구분 코드)
    FID_COND_SCR_DIV_CODE: str = '16634'  # 조건화면분류코드 16634(Primary key)
    FID_INPUT_ISCD: str # 입력종목코드 회원사코드 (kis developers 포탈 사이트 포럼-> FAQ -> 종목정보 다운로드(국내) 참조)
    FID_DIV_CLS_CODE: str = '0' # 분류구분코드 전체(0) 매수(1) 중립(2) 매도(3)
    FID_INPUT_DATE_1: str # 입력날짜1 이후 ~
    FID_INPUT_DATE_2: str # 입력날짜2 ~ 이전

class InvestOpbysecItem(StockApiBaseModel):
    stck_bsop_date: str # 주식영업일자 
    stck_shrn_iscd: str # 주식단축종목코드 
    hts_kor_isnm: str # HTS한글종목명 
    invt_opnn: str # 투자의견 
    invt_opnn_cls_code: str # 투자의견구분코드 
    rgbf_invt_opnn: str # 직전투자의견 
    rgbf_invt_opnn_cls_code: str # 직전투자의견구분코드 
    mbcr_name: str # 회원사명 
    stck_prpr: str # 주식현재가 
    prdy_vrss: str # 전일대비 
    prdy_vrss_sign: str # 전일대비부호 
    prdy_ctrt: str # 전일대비율 
    hts_goal_prc: str # HTS목표가격 
    stck_prdy_clpr: str # 주식전일종가 
    stft_esdg: str # 주식선물괴리도 
    dprt: str # 괴리율 

class InvestOpbysec_Response(StockApiBaseModel):
    rt_cd: str # 성공 실패 여부 
    msg_cd: str # 응답코드 
    msg1: str # 응답메세지 
    output1: List[InvestOpbysecItem]