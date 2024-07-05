# logs_model.py
from datetime import datetime
from typing import Optional
from beanie import Document
from pydantic import BaseModel, Field

class LogQueryParams(BaseModel):
    ''' 로그 조회 쿼리 파라미터 '''
    start_ymd: Optional[str] = Field(None, pattern=r"^\d{8}$")
    end_ymd: Optional[str] = Field(None, pattern=r"^\d{8}$")
    user_id: Optional[str] = None
    acct_no: Optional[bool] = None
    stk_abbr: Optional[str] = None

    def to_query_dict(self) -> dict:
        query = {}
        
        if self.start_ymd and self.end_ymd:
            start_date = datetime.strptime(self.start_ymd, "%Y%m%d")
            end_date = datetime.strptime(self.end_ymd, "%Y%m%d")
            query["at_time"] = {"$gte": start_date, "$lte": end_date}
        elif self.start_ymd:
            start_date = datetime.strptime(self.start_ymd, "%Y%m%d")
            query["at_time"] = {"$gte": start_date}
        elif self.end_ymd:
            end_date = datetime.strptime(self.end_ymd, "%Y%m%d")
            query["at_time"] = {"$lte": end_date}

        if self.user_id:
            query["user_id"] = self.user_id
        if self.acct_no is not None:
            query["acct_no"] = self.acct_no
        if self.stk_abbr:
            query["stk_abbr"] = self.stk_abbr
        
        return query


class LogsRequest(BaseModel):
    at_time: datetime = Field(default_factory=datetime.now)
    user_id: Optional[str] = None
    stk_abbr: Optional[str] = None
    acct_no: Optional[bool] = False
    message: str

class Logs(Document):
    at_time: datetime = Field(default_factory=datetime.now)
    user_id: Optional[str] = None
    stk_abbr: Optional[str] = None
    acct_no: Optional[bool] = False
    message: str

    class Settings:
        name = "Logs"