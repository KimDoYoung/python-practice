from pydantic import BaseModel
from typing import Optional

class Ifi10LawBase(BaseModel):
    ifi10_law_cd: Optional[str]
    ifi10_law_nm: Optional[str]
    ifi10_relevant_law: Optional[str]
    ifi10_submission: Optional[str]
    ifi10_cycle_type: Optional[str]
    ifi10_term_type: Optional[str]

class Ifi10LawCreate(Ifi10LawBase):
    pass

class Ifi10LawResponse(Ifi10LawBase):
    ifi10_law_id: int

    class Config:
        model_config = {
            'from_attributes': True  # ORM 모드 활성화
        }
