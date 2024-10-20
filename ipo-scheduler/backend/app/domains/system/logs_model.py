# logs_model.py
"""
모듈 설명: 
    - Logs 모델
주요 기능:
    - 단타 동작 중 발생하는 로그
    - 스케줄(cron) 작업 중 발생하는 로그

작성자: 김도영
작성일: 2024-07-20
버전: 1.0
"""
from datetime import datetime
from typing import Literal
from beanie import Document
from pydantic import Field, field_validator


class Logs(Document):
    gubun: Literal["Danta", "Cron"]
    level: Literal["Error", "Info"]
    title: str
    detail: str
    upd_time: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    class Settings:
        collection = "Logs"

    @field_validator('upd_time', mode='before')
    def set_upd_time(cls, v):
        return v or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
