# 주식현재가 일자별

from typing import List
from backend.app.domains.stock_api_base_model import StockApiBaseModel


class InquireDailyPrice_Request(StockApiBaseModel):
    FID_COND_MRKT_DIV_CODE: str = 'J' # FID 조건 시장 분류 코드 J : 주식, ETF, ETN
    FID_INPUT_ISCD: str # FID 입력 종목코드 종목번호 (6자리) ETN의 경우, Q로 시작 (EX. Q500001)
    FID_PERIOD_DIV_CODE: str # FID 기간 분류 코드 D : (일)최근 30거래일 W : (주)최근 30주 M : (월)최근 30개월
    FID_ORG_ADJ_PRC: str = '1' # FID 수정주가 원주가 가격 0 : 수정주가반영 1 : 수정주가미반영 * 수정주가는 액면분할/액면병합 등 권리 발생 시 과거 시세를 현재 주가에 맞게 보정한 가격

class InquireDailyPriceItem(StockApiBaseModel):
    stck_bsop_date: str # 주식 영업 일자 
    stck_oprc: str # 주식 시가 
    stck_hgpr: str # 주식 최고가 
    stck_lwpr: str # 주식 최저가 
    stck_clpr: str # 주식 종가 
    acml_vol: str # 누적 거래량 
    prdy_vrss_vol_rate: str # 전일 대비 거래량 비율 
    prdy_vrss: str # 전일 대비 
    prdy_vrss_sign: str # 전일 대비 부호 1 : 상한 2 : 상승 3 : 보합 4 : 하한 5 : 하락
    prdy_ctrt: str # 전일 대비율 
    hts_frgn_ehrt: str # HTS 외국인 소진율 
    frgn_ntby_qty: str # 외국인 순매수 수량 
    flng_cls_code: str # 락 구분 코드 01 : 권리락 02 : 배당락 03 : 분배락 04 : 권배락 05 : 중간(분기)배당락 06 : 권리중간배당락 07 : 권리분기배당락
    acml_prtt_rate: str # 누적 분할 비율 

class InquireDailyPrice_Response(StockApiBaseModel):
    rt_cd: str # 성공 실패 여부 0 : 성공 0 이외의 값 : 실패
    msg_cd: str # 응답코드 응답코드
    msg1: str # 응답메세지 응답메세지
    output: List[InquireDailyPriceItem]