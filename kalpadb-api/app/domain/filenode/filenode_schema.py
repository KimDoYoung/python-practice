from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ApNodeBase(BaseModel):
    node_type: str
    parent_id: Optional[str]
    name: Optional[str]
    full_name: Optional[str]
    owner_id: str
    group_auth: str
    guest_auth: str
    delete_yn: Optional[str] = "N"

class ApNodeCreate(ApNodeBase):
    pass

class ApNodeResponse(ApNodeBase):
    id: str
    create_dt: datetime
    modify_dt: Optional[datetime]
    upload_id: Optional[str]

    model_config = {
        'from_attributes': True  # ORM 모드 활성화
    }
    
class ApFileBase(BaseModel):
    parent_node_id: str
    saved_dir_name: str
    saved_file_name: str
    org_file_name: str
    file_size: int
    content_type: Optional[str]
    hashcode: Optional[str]
    note: Optional[str]
    width: Optional[int]
    height: Optional[int]

class ApFileCreate(ApFileBase):
    pass

class ApFileResponse(ApFileBase):
    node_id: str
    upload_dt: datetime

    model_config = {
        'from_attributes': True  # ORM 모드 활성화
    }

class MatchFileVarBase(BaseModel):
    tbl: str
    id: str
    node_id: str

class MatchFileVarResponse(MatchFileVarBase):
    model_config = {
        'from_attributes': True  # ORM 모드 활성화
    }

class MatchFileIntBase(BaseModel):
    tbl: str
    id: int
    node_id: str

class MatchFileIntResponse(MatchFileIntBase):
    model_config = {
        'from_attributes': True  # ORM 모드 활성화
    }
    
class AttachFileInfo(BaseModel):
    node_id: str
    file_name : str
    file_size: int
    url : str 
    width: Optional[int]
    height: Optional[int]   

class FileNoteData(BaseModel):
    node_id: str
    note: str