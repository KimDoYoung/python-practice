from pydantic import BaseModel
from typing import Optional

class Ifi92ApiLayoutBase(BaseModel):
    ifi92_layout_cd: str
    ifi92_message_cd: Optional[str]
    ifi92_seq: Optional[int]
    ifi92_component_cd: Optional[str]
    ifi92_element_nm: Optional[str]
    ifi92_element_knm: Optional[str]
    ifi92_data_type: Optional[str]
    ifi92_required_yn: Optional[str]
    ifi92_data_length: Optional[int]
    ifi92_description: Optional[str]
    ifi92_note: Optional[str]
    ifi92_link_column: Optional[str]
    ifi92_link_column_type: Optional[str]
    ifi92_link_column_conv_cd: Optional[str]

class Ifi92ApiLayoutCreate(Ifi92ApiLayoutBase):
    pass

class Ifi92ApiLayoutResponse(Ifi92ApiLayoutBase):
    ifi92_api_layout_id: int

    class Config:
        model_config = {
            'from_attributes': True  # ORM 모드 활성화
        }
