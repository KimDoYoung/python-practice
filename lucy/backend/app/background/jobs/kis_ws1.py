
import asyncio
from datetime import datetime
import json
import websockets
from beanie import init_beanie
import requests
from backend.app.core.config import config
from backend.app.core.mongodb import MongoDb
from backend.app.domains.user.user_model import User
from backend.app.core.dependency import get_user_service
from backend.app.core.logger import get_logger

logger = get_logger(__name__)

async def init_db():
    ''' Lucy가 사용하는 stockdb 초기화 '''
    mongodb_url = config.DB_URL 
    db_name = config.DB_NAME
    await MongoDb.initialize(mongodb_url)
    
    db = MongoDb.get_client()[db_name]
    await init_beanie(database=db, document_models=[User])

def get_ws_approval_key(key, secret):
    # url = https://openapivts.koreainvestment.com:29443' # 모의투자계좌     
    url = 'https://openapi.koreainvestment.com:9443' # 실전투자계좌
    headers = {"content-type": "application/json"}
    body = {"grant_type": "client_credentials",
            "appkey": key,
            "secretkey": secret}
    PATH = "oauth2/Approval"
    URL = f"{url}/{PATH}"
    res = requests.post(URL, headers=headers, data=json.dumps(body))
    logger.debug("웹소켓 접속키 발급 결과 : " + res.text)    
    approval_key = res.json()["approval_key"]
    return approval_key

async def kis_ws_connect():
    await init_db()
    user_service = get_user_service()
    user = await user_service.get_1("kdy987")
    
    KIS_APP_KEY = user.get_value_by_key("KIS_APP_KEY")
    KIS_APP_SECRET = user.get_value_by_key("KIS_APP_SECRET")
    KIS_HTS_USER_ID = user.get_value_by_key("KIS_HTS_USER_ID")
    kis_ws_url = 'ws://ops.koreainvestment.com:21000'
    custtype = 'P'

    ws_approval_key = get_ws_approval_key(KIS_APP_KEY, KIS_APP_SECRET)

    print(f"ws access key :[{ws_approval_key}]")
    
    async with websockets.connect(kis_ws_url, ping_interval=None) as websocket:

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        choice = input(timestamp + ": Enter 'exit' to exit: ")
        stk_code = '005930'
        if choice == '1': #주식호가 등록
            tr_id = 'H0STASP0'
            tr_type = '1'
        else:
            senddata = 'wrong inert data'
        
        if choice == '1':
            senddata = '{{"header": {{"approval_key": "{}", "personalseckey": "{}", "custtype": "P", "tr_type": "{}", "content-type": "utf-8"}}, "body": {{"input": {{"tr_id": "{}", "tr_key": "{}"}}}}}}'.format(
                ws_approval_key, KIS_APP_SECRET, tr_type, tr_id, stk_code
            )
            logger.info("senddata : " + senddata)
        #TODO https://github.com/koreainvestment/open-trading-api/blob/main/websocket/python/ops_ws_sample.py#L29 소스 좀더 참고해보기
        await websocket.send(senddata)
        while True:
            response = await websocket.recv()
            logger.info("웹소켓(KIS로부터 받은데이터) : [" + response + "]")
            if response[0] == '0' or response[0] == '1': #실시간데이터
                json_data = json.loads(response)
                tr_id = json_data['header']['tr_id']
                
            else:
                json_data = json.loads(response)
                tr_id = json_data['header']['tr_id']
                if tr_id != 'PINGPONG':
                    logger.debug("tr_id : " + tr_id)
                elif tr_id == 'PINGPONG':
                    logger.debug("PINGPONG데이터 받음: [" + response + "]")
                    await websocket.pong(response)
                    logger.debug("PINGPONG데이터 전송: [" + response + "]")
                


def run():
    # 비동기로 서버에 접속한다.
    asyncio.get_event_loop().run_until_complete(kis_ws_connect())
    asyncio.get_event_loop().close()    

if __name__ == "__main__":
    run()