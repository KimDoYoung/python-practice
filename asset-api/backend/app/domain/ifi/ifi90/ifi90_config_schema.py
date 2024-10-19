from pydantic import BaseModel
from typing import Optional

class Ifi90ConfigBase(BaseModel):
    ifi90_if_cd: Optional[str]
    ifi90_if_nm: Optional[str]
    ifi90_if_type: Optional[str]
    ifi90_local_ip: Optional[str]
    ifi90_local_port: Optional[str]
    ifi90_local_account: Optional[str]
    ifi90_local_pw: Optional[str]
    ifi90_local_path: Optional[str]
    ifi90_local_key: Optional[str]
    ifi90_target_ip: Optional[str]
    ifi90_target_port: Optional[str]
    ifi90_target_account: Optional[str]
    ifi90_target_pw: Optional[str]
    ifi90_target_path: Optional[str]
    ifi90_target_key: Optional[str]
    ifi90_note: Optional[str]

class Ifi90ConfigCreate(Ifi90ConfigBase):
    pass

class Ifi90ConfigResponse(Ifi90ConfigBase):
    ifi90_config_id: int

    class Config:
        orm_mode = True  # 반드시 orm_mode를 활성화해야 함
        from_attributes = True  # from_orm 사용을 위한 설정 추가
