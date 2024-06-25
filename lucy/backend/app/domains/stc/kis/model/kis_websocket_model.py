import json
from typing import List, Optional, Type, TypeVar
from pydantic import BaseModel, ValidationError

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
    output: Optional[Output] = None

class Header(BaseModel):
    tr_id: str
    tr_key: str
    encrypt: str

class KisWsResponse(KisWsResponseBase):
    header: Header
    body: Body

    def isPingPong(self) -> bool:
        return self.header.tr_id == 'PINGPONG'

class KisWsRealHeader(BaseModel):
    ''' KIS의 실시간 데이터 헤더 모델'''
    encrypt: str # 1) 암호화 유무 (0 : 암호화 되지 않은 데이터, 1: 암호화된 데이터)
    tr_id: str   # 2) TR_ID (등록한 tr_id)
    data_count: int # 3) 데이터 건수 (ex. 001)

    @classmethod
    def from_text(cls, text: str) -> "KisWsRealHeader":
        fields = text.split('|')
        return cls(
            encrypt=fields[0],
            tr_id=fields[1],
            data_count=int(fields[2])
        )

    def is_encrypted(self) -> bool:
        return self.encrypt == '1'
    
class KisWsRealModelBase(BaseModel):
    ''' KIS의 실시간 데이터 모델 슈퍼 클래스'''
    def to_str(self) -> str:
        """객체를 문자열로 변환"""
        return str(self.model_dump())

    def to_json(self) -> str:
        """객체를 JSON 문자열로 변환"""
        return json.dumps(self.model_dump(), ensure_ascii=False)
    
    def to_dict(self) -> dict:
        """객체를 dict로 변환"""
        return self.model_dump()
#
# 호가 실시간데이터
# https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock-real2#L_9cda726b-6f0b-48b5-8369-6d66bea05a2a
#     

class CostQty(BaseModel):
    가격: int
    잔량: int

class H0STASP0(KisWsRealModelBase):
    단축종목코드: str
    영업시간: str
    시간구분코드: str
    매도호가배열: List[CostQty]
    매수호가배열: List[CostQty]
    # 매도호가잔량배열: List[int]
    # 매수호가잔량배열: List[int]
    
    총매도호가_잔량: int # = Field(..., alias='TOTAL_ASKP_RSQN')
    총매수호가_잔량: int # = Field(..., alias='TOTAL_BIDP_RSQN')
    시간외_총매도호가_잔량: int #= Field(..., alias='OVTM_TOTAL_ASKP_RSQN')
    시간외_총매수호가_잔량: int #= Field(..., alias='OVTM_TOTAL_BIDP_RSQN')
    예상_체결가: int #= Field(..., alias='ANTC_CNPR')
    예상_체결량: int #= Field(..., alias='ANTC_CNQN')
    예상_거래량: int #= Field(..., alias='ANTC_VOL')
    예상_체결_대비: int #= Field(..., alias='ANTC_CNTG_VRSS')
    예상_체결_대비부호: str #= Field(..., alias='ANTC_CNTG_VRSS_SIGN')
    예상_체결_전일대비율: float #= Field(..., alias='ANTC_CNTG_PRDY_CTRT')
    누적_거래량: int #= Field(..., alias='ACML_VOL')
    총매도호가_잔량_증감: int #= Field(..., alias='TOTAL_ASKP_RSQN_ICDC')
    총매수호가_잔량_증감: int #= Field(..., alias='TOTAL_BIDP_RSQN_ICDC')
    시간외_총매도호가_잔량_증감: int #= Field(..., alias='OVTM_TOTAL_ASKP_ICDC')
    시간외_총매수호가_잔량_증감: int #= Field(..., alias='OVTM_TOTAL_BIDP_ICDC')
    주식매매_구분코드: str #= Field(..., alias='STCK_DEAL_CLS_CODE')
    
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
            매수호가배열=매수호가,
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
    
#
# 체결가 실시간데이터
# https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock-real2#L_714d1437-8f62-43db-a73c-cf509d3f6aa7
#

class H0STCNT0(KisWsRealModelBase):
    유가증권_단축_종목코드: str # MKSC_SHRN_ISCD
    주식_체결_시간: str # STCK_CNTG_HOUR
    주식_현재가: int # STCK_PRPR, 체결가격
    전일_대비_부호: str # PRDY_VRSS_SIGN, 1 : 상한, 2 : 상승, 3 : 보합, 4 : 하한, 5 : 하락
    전일_대비: int # PRDY_VRSS
    전일_대비율: float # PRDY_CTRT
    가중_평균_주식_가격: float # WGHN_AVRG_STCK_PRC
    주식_시가: int # STCK_OPRC
    주식_최고가: int # STCK_HGPR
    주식_최저가: int # STCK_LWPR
    매도호가1: int # ASKP1
    매수호가1: int # BIDP1
    체결_거래량: int # CNTG_VOL
    누적_거래량: int # ACML_VOL
    누적_거래_대금: int # ACML_TR_PBMN
    매도_체결_건수: int # SELN_CNTG_CSNU
    매수_체결_건수: int # SHNU_CNTG_CSNU
    순매수_체결_건수: int # NTBY_CNTG_CSNU
    체결강도: float # CTTR
    총_매도_수량: int # SELN_CNTG_SMTN
    총_매수_수량: int # SHNU_CNTG_SMTN
    체결구분: str # CCLD_DVSN, 1:매수(+) , 3:장전 , 5:매도(-)
    매수비율: float # SHNU_RATE
    전일_거래량_대비_등락율: float # PRDY_VOL_VRSS_ACML_VOL_RATE
    시가_시간: str # OPRC_HOUR
    시가대비구분: str # OPRC_VRSS_PRPR_SIGN, 1 : 상한, 2 : 상승, 3 : 보합, 4 : 하한, 5 : 하락
    시가대비: int # OPRC_VRSS_PRPR
    최고가_시간: str # HGPR_HOUR
    고가대비구분: str # HGPR_VRSS_PRPR_SIGN, 1 : 상한, 2 : 상승, 3 : 보합, 4 : 하한, 5 : 하락
    고가대비: int # HGPR_VRSS_PRPR
    최저가_시간: str # LWPR_HOUR
    저가대비구분: str # LWPR_VRSS_PRPR_SIGN, 1 : 상한, 2 : 상승, 3 : 보합, 4 : 하한, 5 : 하락
    저가대비: int # LWPR_VRSS_PRPR
    영업_일자: str # BSOP_DATE
    신_장운영_구분_코드: str # NEW_MKOP_CLS_CODE, (1) 첫 번째 비트 1 : 장개시전, 2 : 장중, 3 : 장종료후, 4 : 시간외단일가, 7 : 일반Buy-in, 8 : 당일Buy-in; (2) 두 번째 비트 0 : 보통, 1 : 종가, 2 : 대량, 3 : 바스켓, 7 : 정리매매, 8 : Buy-in
    거래정지_여부: str # TRHT_YN, Y : 정지, N : 정상거래
    매도호가_잔량1: int # ASKP_RSQN1
    매수호가_잔량1: int # BIDP_RSQN1
    총_매도호가_잔량: int # TOTAL_ASKP_RSQN
    총_매수호가_잔량: int # TOTAL_BIDP_RSQN
    거래량_회전율: float # VOL_TNRT
    전일_동시간_누적_거래량: int # PRDY_SMNS_HOUR_ACML_VOL
    전일_동시간_누적_거래량_비율: float # PRDY_SMNS_HOUR_ACML_VOL_RATE
    시간_구분_코드: str # HOUR_CLS_CODE, 0 : 장중, A : 장후예상, B : 장전예상, C : 9시이후의 예상가, VI발동, D : 시간외 단일가 예상
    임의종료구분코드: str # MRKT_TRTM_CLS_CODE
    정적VI발동기준가: int # VI_STND_PRC

    @classmethod
    def from_text(cls, text: str) -> "H0STCNT0":
        fields = text.strip().split('^')
        return cls(
            유가증권_단축_종목코드=fields[0],
            주식_체결_시간=fields[1],
            주식_현재가=int(fields[2]),
            전일_대비_부호=fields[3],
            전일_대비=int(fields[4]),
            전일_대비율=float(fields[5]),
            가중_평균_주식_가격=float(fields[6]),
            주식_시가=int(fields[7]),
            주식_최고가=int(fields[8]),
            주식_최저가=int(fields[9]),
            매도호가1=int(fields[10]),
            매수호가1=int(fields[11]),
            체결_거래량=int(fields[12]),
            누적_거래량=int(fields[13]),
            누적_거래_대금=int(fields[14]),
            매도_체결_건수=int(fields[15]),
            매수_체결_건수=int(fields[16]),
            순매수_체결_건수=int(fields[17]),
            체결강도=float(fields[18]),
            총_매도_수량=int(fields[19]),
            총_매수_수량=int(fields[20]),
            체결구분=fields[21],
            매수비율=float(fields[22]),
            전일_거래량_대비_등락율=float(fields[23]),
            시가_시간=fields[24],
            시가대비구분=fields[25],
            시가대비=int(fields[26]),
            최고가_시간=fields[27],
            고가대비구분=fields[28],
            고가대비=int(fields[29]),
            최저가_시간=fields[30],
            저가대비구분=fields[31],
            저가대비=int(fields[32]),
            영업_일자=fields[33],
            신_장운영_구분_코드=fields[34],
            거래정지_여부=fields[35],
            매도호가_잔량1=int(fields[36]),
            매수호가_잔량1=int(fields[37]),
            총_매도호가_잔량=int(fields[38]),
            총_매수호가_잔량=int(fields[39]),
            거래량_회전율=float(fields[40]),
            전일_동시간_누적_거래량=int(fields[41]),
            전일_동시간_누적_거래량_비율=float(fields[42]),
            시간_구분_코드=fields[43],
            임의종료구분코드=fields[44] if fields[44] else "", # 빈값 처리
            정적VI발동기준가=int(fields[45])
        )

#
# 실시간체결통보
# https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock-real2#L_1e3c056d-1b42-461c-b8fb-631bb48e1ee2
#

class H0STCNI0(KisWsRealModelBase):
    고객_ID: str  # CUST_ID, 고객 ID
    계좌번호: str  # ACNT_NO, 계좌번호
    주문번호: str  # ODER_NO, 주문번호
    원주문번호: str  # OODER_NO, 원주문번호
    매도매수구분: str  # SELN_BYOV_CLS, 매도매수구분: 01 : 매도, 02 : 매수
    정정구분: str  # RCTF_CLS, 정정구분
    주문종류: str  # ODER_KIND, 주문종류: 주문통보: 주문낸 주문종류로 수신 / 체결통보: 00으로 수신
    주문조건: str  # ODER_COND, 주문조건
    주식_단축_종목코드: str  # STCK_SHRN_ISCD, 주식 단축 종목코드
    체결_수량: str  # CNTG_QTY, 체결 수량: 체결통보(CNTG_YN=2): 체결 수량, 주문·정정·취소·거부 접수 통보(CNTG_YN=1): 주문수량
    체결단가: str  # CNTG_UNPR, 체결단가
    주식_체결_시간: str  # STCK_CNTG_HOUR, 주식 체결 시간
    거부여부: str  # RFUS_YN, 거부여부: 0 : 승인, 1 : 거부
    체결여부: str  # CNTG_YN, 체결여부: 1 : 주문,정정,취소,거부, 2 : 체결 (★ 체결만 보실경우 2번만 보시면 됩니다)
    접수여부: str  # ACPT_YN, 접수여부: 1 : 주문접수, 2 : 확인, 3: 취소(FOK/IOC)
    지점번호: str  # BRNC_NO, 지점번호
    주문수량: str  # ODER_QTY, 주문수량
    계좌명: str  # ACNT_NAME, 계좌명
    체결종목명: str  # CNTG_ISNM, 체결종목명
    신용구분: str  # CRDT_CLS, 신용구분
    신용대출일자: str  # CRDT_LOAN_DATE, 신용대출일자
    체결종목명40: str  # CNTG_ISNM40, 체결종목명40
    주문가격: str  # ODER_PRC, 주문가격: 체결통보(CNTG_YN=2): 주문 가격, 주문·정정·취소·거부 접수 통보(CNTG_YN=1): 체결단가(빈값으로 수신)

    @classmethod
    def from_text(cls, text: str) -> "H0STCNI0":
        fields = text.strip().split('^')
        return cls(
            고객_ID=fields[0],
            계좌번호=fields[1],
            주문번호=fields[2],
            원주문번호=fields[3],
            매도매수구분=fields[4],
            정정구분=fields[5],
            주문종류=fields[6],
            주문조건=fields[7],
            주식_단축_종목코드=fields[8],
            체결_수량=fields[9],
            체결단가=fields[10],
            주식_체결_시간=fields[11],
            거부여부=fields[12],
            체결여부=fields[13],
            접수여부=fields[14],
            지점번호=fields[15],
            주문수량=fields[16],
            계좌명=fields[17],
            체결종목명=fields[18],
            신용구분=fields[19],
            신용대출일자=fields[20],
            체결종목명40=fields[21],
            주문가격=fields[22],
        )