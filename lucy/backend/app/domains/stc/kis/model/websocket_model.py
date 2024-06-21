import json
from typing import List, Type, TypeVar
from pydantic import BaseModel, Field, ValidationError

T = TypeVar('T', bound='KisWsResponseBase')

class KisWsResponseBase(BaseModel):
    '''KIS 웹소켓 응답 데이터 모델'''

    @classmethod
    def from_json_str(cls: Type[T], json_str: str) -> T:
        try:
            json_dict = json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"웹소켓 데이터 처리 오류: Invalid JSON data: {e}")
        
        try:
            return cls.model_validate(json_dict)
        except ValidationError as e:
            raise ValueError(f"웹소켓 데이터 처리 오류 : Validation error: {e}")

class Output(BaseModel):
    iv: str
    key: str

class Body(BaseModel):
    rt_cd: str
    msg_cd: str
    msg1: str
    output: Output

class Header(BaseModel):
    tr_id: str
    tr_key: str
    encrypt: str

class KisWsResponse(KisWsResponseBase):
    header: Header
    body: Body

    def isPingPong(self) -> bool:
        return self.header.tr_id == 'PINGPONG'
    
#
# 호가 실시간데이터
#     

class CostQty(BaseModel):
    가격: int
    잔량: int

class H0STASP0(BaseModel):
    단축종목코드: str
    영업시간: str
    시간구분코드: str
    매도호가배열: List[CostQty]
    매수호가배열: List[CostQty]
    # 매도호가잔량배열: List[int]
    # 매수호가잔량배열: List[int]
    
    총매도호가_잔량: int = Field(..., alias='TOTAL_ASKP_RSQN')
    총매수호가_잔량: int = Field(..., alias='TOTAL_BIDP_RSQN')
    시간외_총매도호가_잔량: int = Field(..., alias='OVTM_TOTAL_ASKP_RSQN')
    시간외_총매수호가_잔량: int = Field(..., alias='OVTM_TOTAL_BIDP_RSQN')
    예상_체결가: int = Field(..., alias='ANTC_CNPR')
    예상_체결량: int = Field(..., alias='ANTC_CNQN')
    예상_거래량: int = Field(..., alias='ANTC_VOL')
    예상_체결_대비: int = Field(..., alias='ANTC_CNTG_VRSS')
    예상_체결_대비부호: str = Field(..., alias='ANTC_CNTG_VRSS_SIGN')
    예상_체결_전일대비율: float = Field(..., alias='ANTC_CNTG_PRDY_CTRT')
    누적_거래량: int = Field(..., alias='ACML_VOL')
    총매도호가_잔량_증감: int = Field(..., alias='TOTAL_ASKP_RSQN_ICDC')
    총매수호가_잔량_증감: int = Field(..., alias='TOTAL_BIDP_RSQN_ICDC')
    시간외_총매도호가_잔량_증감: int = Field(..., alias='OVTM_TOTAL_ASKP_ICDC')
    시간외_총매수호가_잔량_증감: int = Field(..., alias='OVTM_TOTAL_BIDP_ICDC')
    주식매매_구분코드: str = Field(..., alias='STCK_DEAL_CLS_CODE')
    
    @classmethod
    def from_text(cls, text: str) -> "H0STASP0":
        recvvalue = text.strip().split('^')
        매도호가 = [CostQty(가격=int(recvvalue[i]), 잔량=int(recvvalue[23 + i])) for i in range(3, 13)]
        매수호가 = [CostQty(가격=int(recvvalue[13 + i]), 잔량=int(recvvalue[33 + i])) for i in range(10)]
        
        return cls(
            단축종목코드=recvvalue[0],
            영업시간=recvvalue[1],
            시간구분코드=recvvalue[2],
            매도호가배열=매도호가,
            매도호가배열=매수호가,
            총매도호가_잔량=int(recvvalue[43]),
            총매도호가_잔량_증감=int(recvvalue[54]),
            총매수호가_잔량=int(recvvalue[44]),
            총매수호가_잔량_증감=int(recvvalue[55]),
            시간외_총매도호가_잔량=int(recvvalue[45]),
            시간외_총매수호가_잔량=int(recvvalue[46]),
            시간외_총매도호가_잔량_증감=int(recvvalue[56]),
            시간외_총매수호가_잔량_증감=int(recvvalue[57]),
            예상_체결가=int(recvvalue[47]),
            예상_체결량=int(recvvalue[48]),
            예상_거래량=int(recvvalue[49]),
            예상_체결_대비=int(recvvalue[50]),
            예상_체결_대비부호=recvvalue[51],
            예상_체결_전일대비율=float(recvvalue[52]),
            누적_거래량=int(recvvalue[53]),
            주식매매_구분코드=recvvalue[58]
        )    