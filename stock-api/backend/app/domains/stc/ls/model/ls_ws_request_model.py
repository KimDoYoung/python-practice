# ls_ws_request_model.py
"""
모듈 설명: 
    - LS 증권 websocket Request 모델

작성자: 김도영
작성일: 2024-07-11
버전: 1.0
"""
from pydantic import BaseModel

class Header(BaseModel):
    token: str
    tr_type: str

class Body(BaseModel):
    tr_cd: str
    tr_key: str

class LsWsRequest(BaseModel):
    header: Header
    body: Body