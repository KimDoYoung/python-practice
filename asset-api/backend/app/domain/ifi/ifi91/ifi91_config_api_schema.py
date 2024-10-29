from pydantic import BaseModel
from typing import Optional

class Ifi91ConfigApiBase(BaseModel):
    ifi91_config_id: int
    ifi91_service_type: Optional[str]
    ifi91_api_nm: Optional[str]
    ifi91_path: Optional[str]
    ifi91_http_method: Optional[str]
    ifi91_format: Optional[str]
    ifi91_content_type: Optional[str]
    ifi91_layout_cd: Optional[str]
    ifi91_api_tr_cd: Optional[str]
    ifi91_note: Optional[str]
    ifi91_link_table: Optional[str]
    ifi91_use_yn: Optional[str]

class Ifi91ConfigApiCreate(Ifi91ConfigApiBase):
    pass

class Ifi91ConfigApiResponse(Ifi91ConfigApiBase):
    ifi91_config_api_id: int

    class Config:
        from_attributes = True  # orm_mode 대신 사용됨
        #orm_mode = True