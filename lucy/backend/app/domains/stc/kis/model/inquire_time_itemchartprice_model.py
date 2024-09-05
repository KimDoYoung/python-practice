#주식당일분봉조회
from typing import List
from backend.app.domains.stock_api_base_model import StockApiBaseModel


class InquireTimeItemchartprice_Request(StockApiBaseModel):
    FID_ETC_CLS_CODE: str # FID 기타 구분 코드 기타 구분 코드("")
    FID_COND_MRKT_DIV_CODE: str # FID 조건 시장 분류 코드 시장 분류 코드 (J : 주식, ETF, ETN U: 업종)
    FID_INPUT_ISCD: str # FID 입력 종목코드 종목번호 (6자리) ETN의 경우, Q로 시작 (EX. Q500001)
    FID_INPUT_HOUR_1: str # FID 입력 시간1 조회대상(FID_COND_MRKT_DIV_CODE)에 따라 입력하는 값 상이 종목(J)일 경우, 조회 시작일자(HHMMSS) ex) "123000" 입력 시 12시 30분 이전부터 1분 간격으로 조회 업종(U)일 경우, 조회간격(초) (60 or 120 만 입력 가능) ex) "60" 입력 시 현재시간부터 1분간격으로 조회 "120" 입력 시 현재시간부터 2분간격으로 조회 ※ FID_INPUT_HOUR_1 에 미래일시 입력 시에 현재가로 조회됩니다. ex) 오전 10시에 113000 입력 시에 오전 10시~11시30분 사이의 데이터가 오전 10시 값으로 조회됨
    FID_PW_DATA_INCU_YN: str # FID 과거 데이터 포함 여부 과거 데이터 포함 여부(Y/N) * 업종(U) 조회시에만 동작하는 구분값 N : 당일데이터만 조회 Y : 이후데이터도 조회 (조회시점이 083000(오전8:30)일 경우 전일자 업종 시세 데이터도 같이 조회됨)

class InquireTimeItemchartpriceItem(StockApiBaseModel):
    stck_bsop_date: str # 주식 영업 일자 주식 영업 일자
    stck_cntg_hour: str # 주식 체결 시간 주식 체결 시간
    acml_tr_pbmn: str # 누적 거래 대금 누적 거래 대금
    stck_prpr: str # 주식 현재가 주식 현재가
    stck_oprc: str # 주식 시가2 주식 시가2
    stck_hgpr: str # 주식 최고가 주식 최고가
    stck_lwpr: str # 주식 최저가 주식 최저가
    cntg_vol: str # 체결 거래량 체결 거래량 - 첫번째 배열의 체결량(cntg_vol)은 첫체결이 발생되기 전까지는 이전 분봉의 체결량이 해당 위치에 표시 - 해당 분봉의 첫 체결이 발생되면 해당 이전분 체결량이 두번째 배열로 이동되면서 새로운 체결량으로 업데이트됨 ex) 13:06 의 첫 체결이 13:06:02 발생한 경우  13:06:00 ~ 13:06:01 동안의 13:06 응답의 체결량(cntg_vol)에 13:05 의 체결량(cntg_vol)이 표시됩니다.

class InquireTimeItemchartprice_Response(StockApiBaseModel):
    rt_cd: str # 성공 실패 여부 
    msg_cd: str # 응답코드 
    msg1: str # 응답메세지 
    output2: List[InquireTimeItemchartpriceItem] # 주식당일분봉조회