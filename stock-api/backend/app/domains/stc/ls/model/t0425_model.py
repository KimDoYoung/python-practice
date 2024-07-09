from typing import List, Optional

from backend.app.domains.stock_api_base_model import StockApiBaseModel

class T0425INBLOCK(StockApiBaseModel):
	expcode : str # 종목번호 
	chegb : str = "0" # 체결구분 0;전체 1:체결 2:미체결
	medosu : str = "0" # 매매구분 0:전체 1:매도 2:매수
	sortgb : str = "2" # 정렬순서 1:주문번호 역순 2:주문번호 순
	cts_ordno : str ="" # 주문번호 연속조회시 OutBlock의 동일필드 입력	

class T0425_Request(StockApiBaseModel):
	tr_cont: Optional[str] = 'N'
	tr_cont_key: Optional[str] = ''
	mac_address: Optional[str] = ''
	t0425InBlock : T0425INBLOCK

class T0425OUTBLOCK1(StockApiBaseModel):
    ordno: int # 주문번호 
    expcode: str # 종목번호 
    medosu: str # 구분 
    qty: int # 주문수량 
    price: int # 주문가격 
    cheqty: int # 체결수량 
    cheprice: int # 체결가격 
    ordrem: int # 미체결잔량 
    cfmqty: int # 확인수량 
    status: str # 상태 
    orgordno: int # 원주문번호 
    ordgb: str # 유형 
    ordtime: str # 주문시간 
    ordermtd: str # 주문매체 
    sysprocseq: int # 처리순번 
    hogagb: str # 호가유형 
    price1: int # 현재가 
    orggb: str # 주문구분 
    singb: str # 신용구분 
    loandt: str # 대출일자 	

class T0425OUTBLOCK(StockApiBaseModel):
	tqty: int # 총주문수량 
	tcheqty: int # 총체결수량 
	tordrem: int # 총미체결수량 
	cmss: int # 추정수수료 
	tamt: int # 총주문금액 
	tmdamt: int # 총매도체결금액 
	tmsamt: int # 총매수체결금액 
	tax: int # 추정제세금 
	cts_ordno: str # 주문번호 

class T0425_Response(StockApiBaseModel):
	rsp_cd: str
	rsp_msg: str
	t0425OutBlock: T0425OUTBLOCK
	t0425OutBlock1: List[T0425OUTBLOCK1]