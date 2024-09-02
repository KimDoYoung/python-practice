from typing import List, Optional
from backend.app.domains.stock_api_base_model import StockApiBaseModel

class IntstockStocklistByGroup_Request(StockApiBaseModel):
    TYPE: str # 관심종목구분코드 Unique key(1)
    USER_ID: str # 사용자 ID HTS_ID 입력
    DATA_RANK: str # 데이터 순위 공백
    INTER_GRP_CODE: str # 관심 그룹 코드 관심그룹 조회 결과의 그룹 값 입력
    INTER_GRP_NAME: str # 관심 그룹 명 공백
    HTS_KOR_ISNM: str # HTS 한글 종목명 공백
    CNTG_CLS_CODE: str # 체결 구분 코드 공백
    FID_ETC_CLS_CODE: str # 기타 구분 코드 Unique key(4)

class IntstockStocklistByGroupItem(StockApiBaseModel):
    fid_mrkt_cls_code: str # FID 시장 구분 코드 
    data_rank: str # 데이터 순위 
    exch_code: str # 거래소코드 
    jong_code: str # 종목코드 
    color_code: str # 생상 코드 
    memo: str # 메모 
    hts_kor_isnm: str # HTS 한글 종목명 
    fxdt_ntby_qty: str # 기준일 순매수 수량 
    cntg_unpr: str # 체결단가 
    cntg_cls_code: str # 체결 구분 코드 
    
class IntstockStocklistOutpu1(StockApiBaseModel):
    data_rank: str # 데이터 순위
    inter_grp_name: str # 관심그룹명

class IntstockStocklistByGroup_Response(StockApiBaseModel):
    rt_cd: str # 성공 실패 여부 
    msg_cd: str # 응답코드 
    msg1: str # 응답메세지 
    output1: IntstockStocklistOutpu1
    output2: Optional[List[IntstockStocklistByGroupItem]]=None
