import json
from pydantic import BaseModel

class StockApiBaseModel(BaseModel):
    
    def to_str(self) -> str:
        """객체를 문자열로 변환"""
        return str(self.model_dump())

    def to_json(self) -> str:
        """객체를 JSON 문자열로 변환"""
        return json.dumps(self.model_dump(), ensure_ascii=False)
    
    def to_dict(self) -> dict:
        """객체를 dict로 변환"""
        return self.model_dump()