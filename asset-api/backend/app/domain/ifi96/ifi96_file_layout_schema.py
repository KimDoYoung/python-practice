from pydantic import BaseModel
from typing import Optional

class Ifi96FileLayoutBase(BaseModel):
    ifi96_layout_cd: str
    ifi96_seq: Optional[int]
    ifi96_element_nm: Optional[str]
    ifi96_data_length: Optional[int]
    ifi96_link_column: Optional[str]
    ifi96_link_column_type: Optional[str]
    ifi96_link_column_conv_cd: Optional[str]
    ifi96_required_yn: Optional[str]
    ifi96_note: Optional[str]

class Ifi96FileLayoutCreate(Ifi96FileLayoutBase):
    pass

class Ifi96FileLayoutResponse(Ifi96FileLayoutBase):
    ifi96_file_layout_id: int

    class Config:
        model_config = {
            'from_attributes': True  # ORM 모드 활성화
        }
