# dependency.py
"""
모듈 설명: 
    - DB CRUD를 제공하는 service를 캐싱하는 모듈
주요 기능:
    - 각 테이블(컬렉션)에 대한 CRUD service 객체를 캐싱

작성자: 김도영
작성일: 05
버전: 1.0
"""
from functools import lru_cache

from backend.app.domains.logs.logs_service import LogsService
from backend.app.domains.settings.settings_service import SettingsService
from backend.app.domains.user.user_service import UserService


@lru_cache()
def get_user_service():
    return UserService()

@lru_cache()
def get_logs_service():
    return LogsService()

@lru_cache()
def get_settings_service():
    return SettingsService()
