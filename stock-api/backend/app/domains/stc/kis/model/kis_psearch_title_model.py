from typing import List
from pydantic import BaseModel
from backend.app.domains.stc.kis.model.kis_base_model import KisBaseModel

class PsearchTitleItem(BaseModel):
    user_id: str # HTS ID 
    seq: str # 조건키값 해당 값을 종목조건검색조회 API의 input으로 사용 (0번부터 시작)
    grp_nm: str # 그룹명 HTS(eFriend Plus) [0110] "사용자조건검색"화면을 통해 등록한 사용자조건 그룹
    condition_nm: str # 조건명 등록한 사용자 조건명

class PsearchTitleDto(KisBaseModel):
    '''조건식 목록 조회 결과'''
    rt_cd: str # 성공 실패 여부 
    msg_cd: str # 응답코드 
    msg1: str # 응답메세지 
    output2: List[PsearchTitleItem]