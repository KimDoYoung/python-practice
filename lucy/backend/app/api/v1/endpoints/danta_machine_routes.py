# danta_machine_routes.py
"""
모듈 설명: 
    - danta_machine 관련 API 라우터
주요 기능:
    - /start: 단타머신 시작
    - /stop: 단타머신 종료

작성자: 김도영
작성일: 25
버전: 1.0
"""
from fastapi import APIRouter
from backend.app.background.danta_machine import danta_machine_status, start_danta_machine, stop_danta_machine
from backend.app.core.logger import get_logger
logger = get_logger(__name__)

router = APIRouter()

@router.get("/start")
async def danta_start():
    status = danta_machine_status()
    if status == "stopped":
        await start_danta_machine()  # 비동기 함수 호출
        return {"message": "단타머신 시작되었습니다."}
    else:
        return {"message": "단타머신이 이미 실행 중입니다."}

@router.get("/stop")
async def danta_stop():
    status = danta_machine_status()
    if status == "running":
        await stop_danta_machine()  # 비동기 함수 호출
        return {"message": "단타머신 종료되었습니다."}
    else:
        return {"message": "단타머신이 실행 중이지 않습니다."}

@router.get("/status")
async def danta_status():
    status = danta_machine_status()
    if status == "stopped":
        return {"status": "stopped", "message": "단타머신이 실행 중이 아닙니다."}
    else:
        return {"status": "running", "message": "단타머신이 실행 중입니다."}

#TODO /log log API 추가
#TODO /today
#TODO /status
#TODO danta_event
