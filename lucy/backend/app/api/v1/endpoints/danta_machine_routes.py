import asyncio
from fastapi import APIRouter
from backend.app.background.danta_machine import start_danta_machine
from backend.app.core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()

@router.post("/danta/start")
async def danta_start():
    global danta_machine_task
    if danta_machine_task is None or danta_machine_task.cancelled():
        start_danta_machine()
        return {"message": "단타머신 시작되었습니다."}
    else:
        return {"message": "단타머신이 이미 실행 중입니다."}

@router.post("/danta/stop")
async def danta_stop():
    global danta_machine_task
    if danta_machine_task:
        danta_machine_task.cancel()
        try:
            await danta_machine_task
        except asyncio.CancelledError:
            logger.info("단타머신 종료")
            return {"message": "단타머신 종료되었습니다."}
    return {"message": "단타머신이 실행 중이지 않습니다."}