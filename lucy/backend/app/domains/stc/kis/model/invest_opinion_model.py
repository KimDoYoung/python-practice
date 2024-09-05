# 국내주식 종목투자의견
from typing import List
from backend.app.domains.stock_api_base_model import StockApiBaseModel


class InvestOpinion_Request(StockApiBaseModel):
    FID_COND_MRKT_DIV_CODE: str # 조건시장분류코드 J(시장 구분 코드)
    FID_COND_SCR_DIV_CODE: str # 조건화면분류코드 16633(Primary key)
    FID_INPUT_ISCD: str # 입력종목코드 종목코드(ex) 005930(삼성전자))
    FID_INPUT_DATE_1: str # 입력날짜1 이후 ~(ex) 0020231113)
    FID_INPUT_DATE_2: str # 입력날짜2 ~ 이전(ex) 0020240513)

class InvestOpinionItem(StockApiBaseModel):
    stck_bsop_date: str # 주식영업일자 
    invt_opnn: str # 투자의견 
    invt_opnn_cls_code: str # 투자의견구분코드 
    rgbf_invt_opnn: str # 직전투자의견 
    rgbf_invt_opnn_cls_code: str # 직전투자의견구분코드 
    mbcr_name: str # 회원사명 
    hts_goal_prc: str # HTS목표가격 
    stck_prdy_clpr: str # 주식전일종가 
    stck_nday_esdg: str # 주식N일괴리도 
    nday_dprt: str # N일괴리율 
    stft_esdg: str # 주식선물괴리도 
    dprt: str # 괴리율 

class InvestOpinion_Response(StockApiBaseModel):
    rt_cd: str # 성공 실패 여부 
    msg_cd: str # 응답코드 
    msg1: str # 응답메세지 
    output1: List[InvestOpinionItem]