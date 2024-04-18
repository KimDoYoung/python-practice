
from pydantic import BaseModel, Field
from typing import Optional
from dataclasses import dataclass

@dataclass
class StockPriceRequest(BaseModel):
    serviceKey: Optional[str] = Field(None, description="공공데이터포털에서 받은 인증키")
    numOfRows: Optional[int] = Field(default=10, description="한 페이지 결과 수")
    pageNo: Optional[int] = Field(default=1, description="페이지 번호")
    resultType: Optional[str] = Field(default="xml", description="결과형식, 구분(xml, json)")
    
    basDt: Optional[int] = Field(None, description="검색값과 기준일자가 일치하는 데이터를 검색")
    beginBasDt: Optional[int] = Field(None, description="기준일자가 검색값보다 크거나 같은 데이터를 검색")
    endBasDt: Optional[int] = Field(None, description="기준일자가 검색값보다 작은 데이터를 검색")
    likeBasDt: Optional[int] = Field(None, description="기준일자값이 검색값을 포함하는 데이터를 검색")
    
    likeSrtnCd: Optional[str] = Field(None, description="단축코드가 검색값을 포함하는 데이터를 검색")
    isinCd: Optional[str] = Field(None, description="검색값과 ISIN코드이 일치하는 데이터를 검색")
    likeIsinCd: Optional[str] = Field(None, description="ISIN코드가 검색값을 포함하는 데이터를 검색")
    
    itmsNm: Optional[str] = Field(None, description="검색값과 종목명이 일치하는 데이터를 검색")
    likeItmsNm: Optional[str] = Field(None, description="종목명이 검색값을 포함하는 데이터를 검색")
    mrktCls: Optional[str] = Field(None, description="검색값과 시장구분이 일치하는 데이터를 검색")
    beginVs: Optional[float] = Field(None, description="대비가 검색값보다 크거나 같은 데이터를 검색")
    endVs: Optional[float] = Field(None, description="대비가 검색값보다 작은 데이터를 검색")
    beginFltRt: Optional[float] = Field(None, description="등락률이 검색값보다 크거나 같은 데이터를 검색")
    endFltRt: Optional[float] = Field(None, description="등락률이 검색값보다 작은 데이터를 검색")
    beginTrqu: Optional[int] = Field(None, description="거래량이 검색값보다 크거나 같은 데이터를 검색")
    endTrqu: Optional[int] = Field(None, description="거래량이 검색값보다 작은 데이터를 검색")
    beginTrPrc: Optional[int] = Field(None, description="거래대금이 검색값보다 크거나 같은 데이터를 검색")
    endTrPrc: Optional[int] = Field(None, description="거래대금이 검색값보다 작은 데이터를 검색")
    beginLstgStCnt: Optional[int] = Field(None, description="상장주식수가 검색값보다 크거나 같은 데이터를 검색")
    endLstgStCnt: Optional[int] = Field(None, description="상장주식수가 검색값보다 작은 데이터를 검색")
    beginMrktTotAmt: Optional[int] = Field(None, description="시가총액이 검색값보다 크거나 같은 데이터를 검색")
    endMrktTotAmt: Optional[int] = Field(None, description="시가총액이 검색값보다 작은 데이터를 검색")
