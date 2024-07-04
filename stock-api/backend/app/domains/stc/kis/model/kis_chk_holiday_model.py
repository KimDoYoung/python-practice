from backend.app.domains.stock_api_base_model import StockApiBaseModel


class ChkHolidayItem(StockApiBaseModel):
    bass_dt: str # 기준일자 기준일자(YYYYMMDD)
    wday_dvsn_cd: str # 요일구분코드 01:일요일, 02:월요일, 03:화요일, 04:수요일, 05:목요일, 06:금요일, 07:토요일
    bzdy_yn: str # 영업일여부 Y/N 금융기관이 업무를 하는 날
    tr_day_yn: str # 거래일여부 Y/N 증권 업무가 가능한 날(입출금, 이체 등의 업무 포함)
    opnd_yn: str # 개장일여부 Y/N 주식시장이 개장되는 날 * 주문을 넣고자 할 경우 개장일여부(opnd_yn)를 사용
    sttl_day_yn: str # 결제일여부 Y/N 주식 거래에서 실제로 주식을 인수하고 돈을 지불하는 날

class ChkHolidayDto(StockApiBaseModel):
    rt_cd: str # 성공 실패 여부 
    msg_cd: str # 응답코드 
    msg1: str # 응답메세지 
    output: ChkHolidayItem
