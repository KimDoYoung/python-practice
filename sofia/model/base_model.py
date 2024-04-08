from typing import Optional
from fastapi import Request

class BaseModel:

    def __init__(self, request: Request):
        self.request: Request = request
        self.error: Optional[str] = None

    def to_dict(self) -> dict:
        return self.__dict__