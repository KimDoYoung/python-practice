import json
from pydantic import BaseModel
from typing import Any

from backend.app.domains.stc.kis.kis_mapping import KEY_MAPPING

class KisBaseModel(BaseModel):
    def get(self, key: str) -> Any:
        mapped_key = KEY_MAPPING.get(key, key)
        return getattr(self, mapped_key, None)
    
    def to_str(self) -> str:
        """객체를 문자열로 변환"""
        return str(self.model_dump())

    def to_json(self) -> str:
        """객체를 JSON 문자열로 변환"""
        return json.dumps(self.model_dump(), ensure_ascii=False)
    
    def to_dict(self) -> dict:
        """객체를 dict로 변환"""
        return self.model_dump()