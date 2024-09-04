#국내주식기간별시세(일/주/월/년)[v1_국내주식-016]
from typing import List

from pydantic import Field

from backend.app.domains.stock_api_base_model import StockApiBaseModel

class InquireDailyItemchartprice_Request(StockApiBaseModel):
    FID_COND_MRKT_DIV_CODE: str = 'J' # 시장 분류 코드 J : 주식, ETF, ETN
    FID_INPUT_ISCD: str # 종목코드 종목번호 (6자리) ETN의 경우, Q로 시작 (EX. Q500001)
    FID_INPUT_DATE_1: str # 입력 날짜 (시작) 조회 시작일자 (ex. 20220501)
    FID_INPUT_DATE_2: str # 입력 날짜 (종료) 조회 종료일자 (ex. 20220530) ※ 주(W), 월(M), 년(Y) 봉 조회 시에 아래 참고 ㅁ FID_INPUT_DATE_2 가 현재일 까지일때  . 주봉 조회 : 해당 주의 첫번째 영업일이 포함되어야함  . 월봉 조회 : 해당 월의 전월 일자로 시작되어야함  . 년봉 조회 : 해당 년의 전년도 일자로 시작되어야함 ㅁ FID_INPUT_DATE_2 가 현재일보다 이전일 때  . 주봉 조회 : 해당 주의 첫번째 영업일이 포함되어야함  . 월봉 조회 : 해당 월의 영업일이 포함되어야함  . 년봉 조회 : 해당 년의 영업일이 포함되어야함
    FID_PERIOD_DIV_CODE: str = 'D' # 기간분류코드 D:일봉, W:주봉, M:월봉, Y:년봉
    FID_ORG_ADJ_PRC: str  = '0' # 수정주가 원주가 가격 여부 0:수정주가 1:원주가

class InquireDailyItemchartpriceItem1(StockApiBaseModel):
    prdy_vrss: str  # 전일 대비
    prdy_vrss_sign: str  # 전일 대비 부호
    prdy_ctrt: str  # 전일 대비율
    stck_prdy_clpr: str  # 주식 전일 종가
    acml_vol: str  # 누적 거래량
    acml_tr_pbmn: str  # 누적 거래 대금
    hts_kor_isnm: str  # HTS 한글 종목명
    stck_prpr: str  # 주식 현재가
    stck_shrn_iscd: str  # 주식 단축 종목코드
    prdy_vol: str  # 전일 거래량
    stck_mxpr: str  # 상한가
    stck_llam: str  # 하한가
    stck_oprc: str  # 시가
    stck_hgpr: str  # 최고가
    stck_lwpr: str  # 최저가
    stck_prdy_oprc: str  # 주식 전일 시가
    stck_prdy_hgpr: str  # 주식 전일 최고가
    stck_prdy_lwpr: str  # 주식 전일 최저가
    askp: str  # 매도호가
    bidp: str  # 매수호가
    prdy_vrss_vol: str  # 전일 대비 거래량
    vol_tnrt: str  # 거래량 회전율
    stck_fcam: str  # 주식 액면가
    lstn_stcn: str  # 상장 주수
    cpfn: str  # 자본금
    hts_avls: str  # 시가총액
    per: str  # PER
    eps: str  # EPS
    pbr: str  # PBR
    # 공백이 포함된 키를 매핑
    itewhol_loan_rmnd_ratem_name: str = Field(..., alias="itewhol_loan_rmnd_ratem name") # 전체 융자 잔고 비율


class InquireDailyItemchartpriceItem2(StockApiBaseModel):
    stck_bsop_date: str # 주식 영업 일자 주식 영업 일자
    stck_clpr: str # 주식 종가 주식 종가
    stck_oprc: str # 주식 시가 주식 시가
    stck_hgpr: str # 주식 최고가 주식 최고가
    stck_lwpr: str # 주식 최저가 주식 최저가
    acml_vol: str # 누적 거래량 누적 거래량
    acml_tr_pbmn: str # 누적 거래 대금 누적 거래 대금
    flng_cls_code: str # 락 구분 코드 00:해당사항없음(락이 발생안한 경우) 01:권리락 02:배당락 03:분배락 04:권배락 05:중간(분기)배당락 06:권리중간배당락 07:권리분기배당락
    prtt_rate: str # 분할 비율 분할 비율
    mod_yn: str # 분할변경여부 Y, N
    prdy_vrss_sign: str # 전일 대비 부호 전일 대비 부호
    prdy_vrss: str # 전일 대비 전일 대비
    revl_issu_reas: str # 재평가사유코드 재평가사유코드

class InquireDailyItemchartprice_Response(StockApiBaseModel):
    rt_cd: str # 성공 실패 여부 0 : 성공 0 이외의 값 : 실패
    msg_cd: str # 응답코드 응답코드
    msg1: str # 응답메세지 응답메세지
    output1: InquireDailyItemchartpriceItem1
    output2: List[InquireDailyItemchartpriceItem2]