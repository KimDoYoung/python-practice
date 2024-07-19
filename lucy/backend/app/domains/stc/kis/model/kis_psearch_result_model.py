from pydantic import BaseModel
from typing import List

class PsearchResultItem(BaseModel):
    code: str # 종목코드
    name: str # 종목명
    daebi: str # 전일대비부호 1. 상한 2. 상승 3. 보합 4. 하한 5. 하락
    price: str # 현재가
    chgrate: str # 등락율
    acml_vol: str # 거래량
    trade_amt: str # 거래대금
    change: str # 전일대비
    cttr: str # 체결강도
    open: str # 시가
    high: str # 고가
    low: str # 저가
    high52: str # 52주최고가
    low52: str # 52주최저가
    expprice: str # 예상체결가
    expchange: str # 예상대비
    expchggrate: str # 예상등락률
    expcvol: str # 예상체결수량
    chgrate2: str # 전일거래량대비율
    expdaebi: str # 예상대비부호
    recprice: str # 기준가
    uplmtprice: str # 상한가
    dnlmtprice: str # 하한가
    stotprice: str # 시가총액

class PsearchResult_Response(BaseModel):
    '''조건식 목록 조회 결과'''
    rt_cd: str # 성공 실패 여부
    msg_cd: str # 응답코드
    msg1: str # 응답메세지
    output2: List[PsearchResultItem]
