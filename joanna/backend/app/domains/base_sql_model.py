
from datetime import datetime
import json

from sqlmodel import SQLModel

class BaseSQLModel(SQLModel):
   
    def model_dump_1(self) -> dict:
        """ 모델 데이터를 직렬화 가능한 형태로 변환합니다. """
        data = {}
        for key, value in self.__dict__.items():
            if key.startswith('_'):
                continue  # 내부 및 보호된 속성 제외
            if isinstance(value, datetime):
                data[key] = value.isoformat()  # datetime을 ISO 포맷 문자열로 변환
            else:
                data[key] = value
        return data

    def to_dict(self) -> dict:
        """ Convert instance to dictionary. """
        return self.model_dump_1()

    def to_json(self) -> str:
        """ Convert instance to JSON string. """
        return json.dumps(self.to_dict())

    def to_string(self) -> str:
        """ Return the major information of the instance as a string. """
        return ", ".join(f"{key}={value}" for key, value in self.to_dict().items())
    
class BaseSQLModel1(SQLModel):
    """ 모든 데이터베이스 모델의 기본 클래스입니다. 공통 기능을 제공합니다. """
    
    def model_dump(self):
        """ 모델 데이터를 직렬화 가능한 형태로 변환합니다. """
        data = {}
        #for key, value in self.dict().items():  # self.dict() 사용하여 인스턴스 데이터에 접근
        for key, value in self.__dict__.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()  # datetime을 ISO 포맷 문자열로 변환
            else:
                data[key] = value
        return data

    def to_dict(self):
        """ 인스턴스를 딕셔너리로 변환합니다. """
        return self.model_dump()

    def to_json(self):
        """ 인스턴스를 JSON 문자열로 변환합니다. """
        return json.dumps(self.model_dump())
    
    def to_string(self):
        """ 인스턴스의 주요 정보를 문자열로 반환합니다. """
        return ", ".join(f"{key}={value}" for key, value in self.model_dump().items())
