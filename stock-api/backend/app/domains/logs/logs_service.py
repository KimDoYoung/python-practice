# logs_service.py
"""
모듈 설명: 
    - Logs 컬렉션에 대한 CRUD
주요 기능:
    - get_all
    - create

작성자: 김도영
작성일: 05
버전: 1.0
"""
from typing import List
from backend.app.core.logger import get_logger
from backend.app.domains.logs.logs_model import LogQueryParams, Logs


logger = get_logger(__name__)

class LogsService:
    async def create(self, keyvalue: dict) -> Logs:
        log_entry = Logs(**keyvalue)
        await log_entry.create()
        return log_entry

    async def get_all(self, query_params: LogQueryParams) -> List[Logs]:
        try:
            query = query_params.to_query_dict()
            logs = await Logs.find(query).sort("at_time").to_list()
            return logs
        except Exception as e:
            logger.error(f"Failed to retrieve logs: {e}")
            raise e

    async def count(self) -> int:
        return await Logs.count()
