
import asyncio
from datetime import datetime
import json
import websockets
from beanie import init_beanie
import requests
from backend.app.core.config import config
from backend.app.core.mongodb import MongoDb
from backend.app.domains.stc.kis.model.kis_websocket_model import KisWsResponse
from backend.app.domains.user.user_model import User
from backend.app.core.dependency import get_user_service
from backend.app.core.logger import get_logger
from backend.app.utils.kis_ws_util import is_real_data, real_data_trid

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
            logger.info(f"보낸데이터 : [{senddata}]")
        #TODO https://github.com/koreainvestment/open-trading-api/blob/main/websocket/python/ops_ws_sample.py#L29 소스 좀더 참고해보기
        await websocket.send(senddata)
        while True:
            received_text = await websocket.recv()
            logger.info("웹소켓(KIS로부터 받은데이터) : [" + received_text + "]")
            if is_real_data(received_text): # 실시간 데이터인 경우
                trid0 = real_data_trid(received_text)
                
                # json_data = json.loads(response)
                # tr_id = json_data['header']['tr_id']
                # if response[0] == '0':
                #     recvstr = data.split('|')  # 수신데이터가 실데이터 이전은 '|'로 나뉘어져있어 split
                #     trid0 = recvstr[1]
                #     if trid0 == "H0STASP0":  # 주식호가tr 일경우의 처리 단계
                #         print("#### 주식호가 ####")
                #         stockhoka(recvstr[3])
                #         await asyncio.sleep(1)

                #     elif trid0 == "H0STCNT0":  # 주식체결 데이터 처리
                #         print("#### 주식체결 ####")
                #         data_cnt = int(recvstr[2])	# 체결데이터 개수
                #         stockspurchase(data_cnt, recvstr[3])

                # elif data[0] == '1':
                #     recvstr = data.split('|')  # 수신데이터가 실데이터 이전은 '|'로 나뉘어져있어 split
                #     trid0 = recvstr[1]
                #     if trid0 == "H0STCNI0" or trid0 == "H0STCNI9":  # 주실체결 통보 처리
                #         stocksigningnotice(recvstr[3], aes_key, aes_iv)                
            else: # 실시간 데이터가 아닌 경우
                try:
                    kis_ws_model = KisWsResponse.from_json_str(received_text)

                    if kis_ws_model.isPingPong():
                        await websocket.pong(received_text)  # 웹소켓 클라이언트에서 pong을 보냄
                        logger.debug(f"PINGPONG 데이터 전송: [{received_text}]")
                    else:
                        logger.info(f"PINGPONG 아닌 것: [{received_text}]")
                        logger.debug(f"kis_ws_model: {json.dumps(kis_ws_model.model_dump(), ensure_ascii=False)}")
                except ValueError as e:
                    logger.error(f"Error parsing response: {e}")


def run():
    # 비동기로 서버에 접속한다.
    asyncio.get_event_loop().run_until_complete(kis_ws_connect())
    asyncio.get_event_loop().close()    

if __name__ == "__main__":
    run()