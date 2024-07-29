# fill_ls_stk_info.py
"""
모듈 설명: 
    - LS API master-api 를 통해 주식 정보를 가져와서 DB에 저장하는 모듈
주요 기능:
    - stk_info 컬렉션에 주식 정보를 저장
    - 모두 지우고 다시 저장하는 방식이다.
    
작성자: 김도영
작성일: 2024-07-29
버전: 1.0
"""
import asyncio

from beanie import init_beanie
from backend.app.core.logger import get_logger
from backend.app.core.mongodb import MongoDb
from backend.app.core.config import config
from backend.app.domains.system.stk_info_model import StkInfo
from backend.app.domains.user.user_model import User
from backend.app.managers.stock_api_manager import StockApiManager

from backend.app.core.dependency import get_stkinfo_service

logger = get_logger(__name__)

async def call_master_api_fill_ls_stk_info(arg):
    logger.info("--------------------------------------------------------------")
    logger.info(f" call_master_api_fill_ls_stk_info 시작: {arg}")
    logger.info("--------------------------------------------------------------")
    ls_api = await StockApiManager().stock_api('LS')
    
    response = await ls_api.master_api("1") # 1 코스피, 2 코스닥
    # logger.debug(f"master_api 응답: [{response.to_str()}]")

    list = []
    if response.rsp_cd == '00000':
        for item in response.t9945OutBlock:
            if item.etfchk == '0':
                stk_info = {
                    "stk_code": item.shcode,
                    "stk_name": item.hname,
                    "exp_code": item.expcode,
                    "market": "KSP"
                }
                list.append(stk_info)
            

    response = await ls_api.master_api("2") # 1 코스피, 2 코스닥
    #logger.debug(f"master_api 응답 코스닥: [{response.to_str()}]")

    if response.rsp_cd == '00000':
        for item in response.t9945OutBlock:
            if item.etfchk == '0':
                stk_info = {
                    "stk_code": item.shcode,
                    "stk_name": item.hname,
                    "exp_code": item.expcode,
                    "market": "KSD"
                }
                list.append(stk_info)

    service = get_stkinfo_service()

    await service.delete_all()
            
    for stk_info in list:
        await service.create(stk_info)

    logger.info("--------------------------------------------------------------")
    logger.info(f"DONE!: {arg}")
    logger.info("--------------------------------------------------------------")
    
async def main():
    await MongoDb.initialize(config.DB_URL)
    db = MongoDb.get_client()[config.DB_NAME]
    await init_beanie(database=db, document_models=[User])
    await init_beanie(database=db, document_models=[StkInfo])
    await call_master_api_fill_ls_stk_info("LS stk info 채우기")
    await MongoDb.close()
    print("DONE!")

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        pending = asyncio.all_tasks(loop)
        for task in pending:
            task.cancel()
        loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
        loop.close()
