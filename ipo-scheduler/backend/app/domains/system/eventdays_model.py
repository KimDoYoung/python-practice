from typing import Optional
from beanie import Document

'''
공공데이터에서 가져온 공휴일 정보 및 사용자 지정  eventdays 정보를 저장하는 모델
locdate "20240101"
dateKind "01" 사용자정보는 99
dateName "1월1일"
isHoliday "Y"
seq "1"
isMoon True는 음력
repeat 
'''
class EventDays(Document):
    locdate: str
    dateKind: str
    dateName: str 
    isHoliday: str
    seq: Optional[int] = None
    isMoon: bool = False
    repeat: Optional[str] = None

    class Settings:
        collection = "EventDays"  # 변경된 컬렉션 이름