import json
from typing import Type, TypeVar
from pydantic import BaseModel, ValidationError

T = TypeVar('T', bound='KisWsResponseBase')

class KisWsResponseBase(BaseModel):
    '''KIS 웹소켓 응답 데이터 모델'''

    @classmethod
    def from_json_str(cls: Type[T], json_str: str) -> T:
        try:
            json_dict = json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"웹소켓 데이터 처리 오류: Invalid JSON data: {e}")
        
        try:
            return cls.model_validate(json_dict)
        except ValidationError as e:
            raise ValueError(f"웹소켓 데이터 처리 오류 : Validation error: {e}")

class Output(BaseModel):
    iv: str
    key: str

class Body(BaseModel):
    rt_cd: str
    msg_cd: str
    msg1: str
    output: Output

class Header(BaseModel):
    tr_id: str
    tr_key: str
    encrypt: str

class KisWsResponse(KisWsResponseBase):
    header: Header
    body: Body

    def isPingPong(self) -> bool:
        return self.header.tr_id == 'PINGPONG'