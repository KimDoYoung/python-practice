from pydantic import BaseModel
from typing import Optional

class Ifi95ConfigFileBase(BaseModel):
    ifi95_config_id: int
    ifi95_send_recv_type: Optional[str]
    ifi95_file_nm: Optional[str]
    ifi95_link_table: Optional[str]
    ifi95_separator_cd: Optional[str]
    ifi95_file_layout_cd: Optional[str]
    ifi95_shell: Optional[str]
    ifi95_note: Optional[str]
    ifi95_use_yn: Optional[str]

class Ifi95ConfigFileCreate(Ifi95ConfigFileBase):
    pass

class Ifi95ConfigFileResponse(Ifi95ConfigFileBase):
    ifi95_config_file_id: int

    class Config:
        model_config = {
            'from_attributes': True  # ORM 모드 활성화
        }
