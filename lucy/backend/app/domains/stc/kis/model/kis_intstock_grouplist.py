from typing import List, Optional
from backend.app.domains.stock_api_base_model import StockApiBaseModel


    
class IntstockGrouplistItem(StockApiBaseModel):
    date: str # 일자 
    trnm_hour: str # 전송 시간 
    data_rank: str # 데이터 순위 
    inter_grp_code: str # 관심 그룹 코드 
    inter_grp_name: str # 관심 그룹 명 
    ask_cnt: str # 요청 개수 

class IntstockGrouplist_Response(StockApiBaseModel):
    rt_cd: str # 성공 실패 여부 
    msg_cd: str # 응답코드 
    msg1: str # 응답메세지     
    output2: Optional[List[IntstockGrouplistItem]] = None