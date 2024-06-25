
import asyncio
from datetime import datetime

import websockets
from backend.app.core.logger import get_logger
from backend.app.utils.kis_ws_util import is_real_data
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64decode
import json
import requests
import websockets
from beanie import init_beanie
from backend.app.core.config import config
from backend.app.core.mongodb import MongoDb
from backend.app.domains.stc.kis.model.kis_websocket_model import H0STASP0, H0STCNI0, H0STCNT0, KisWsRealHeader, KisWsResponse
from backend.app.domains.stc.kis.model.kis_ws_request_model import Body, Header, Input, KisWsRequest
from backend.app.domains.user.user_model import User
from backend.app.core.dependency import get_user_service

logger = get_logger(__name__)


async def init_db():
    ''' Lucy가 사용하는 stockdb 초기화 '''
    mongodb_url = config.DB_URL 
    db_name = config.DB_NAME
    await MongoDb.initialize(mongodb_url)
    
    db = MongoDb.get_client()[db_name]
    await init_beanie(database=db, document_models=[User])


async def get_ws_approval_key(app_key, app_secret):
    url = 'https://openapi.koreainvestment.com:9443' # 실전투자계좌
    headers = {"content-type": "application/json"}
    body = {"grant_type": "client_credentials",
            "appkey": app_key,
            "secretkey": app_secret}
    PATH = "oauth2/Approval"
    URL = f"{url}/{PATH}"
    res = requests.post(URL, headers=headers, data=json.dumps(body))
    logger.debug("웹소켓 접속키 발급 결과 : " + res.text)    
    approval_key = res.json()["approval_key"]
    return approval_key

def aes_cbc_base64_dec(key, iv, cipher_text):
    """
    :param key:  str type AES256 secret key value
    :param iv: str type AES256 Initialize Vector
    :param cipher_text: Base64 encoded AES256 str
    :return: Base64-AES256 decodec str
    """
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
    return bytes.decode(unpad(cipher.decrypt(b64decode(cipher_text)), AES.block_size))

def kis_ws_real_data_parsing(recv_text, aes_key, aes_iv):
    ''' KisWsRealHeader, KisWsRealModelBase 객체로 변환해서 리턴'''
    class_map = {
        'H0STASP0': H0STASP0,
        'H0STCNT0': H0STCNT0,
        'H0STCNI0': H0STCNI0
    }
    header = KisWsRealHeader.from_text(recv_text)
    body_text = recv_text.split('|', 3)[-1]
    if  header.is_encrypted(): # 암호화된 데이터인 경우
        plain_text = aes_cbc_base64_dec(aes_key, aes_iv, body_text)
    else:
        plain_text = body_text
    
    tr_id = header.tr_id
    instance = None
    if tr_id in class_map:
        cls = class_map[tr_id]
        instance = cls.from_text(plain_text)
        logger.debug(instance)
    else:
        logger.debug(f"{tr_id} 이름의 모델이 존재하지 않습니다.")

    return header, instance

async def handle_websocket(kis_ws_url, req, input_queue):
    async with websockets.connect(kis_ws_url, ping_interval=None) as websocket:
        senddata = req.model_dump_json()
        logger.info(f"보낸데이터 : [{senddata}]")
        await websocket.send(senddata)

        aes_key = None
        aes_iv = None

        while True:
            received_text = await websocket.recv()
            logger.info("웹소켓(KIS로부터 받은 데이터) : [" + received_text + "]")
            if is_real_data(received_text):  # 실시간 데이터인 경우
                header, real_model = kis_ws_real_data_parsing(received_text, aes_key, aes_iv)
                logger.info(f"header: {header}")
                logger.info(f"real_model: {real_model}")
                await asyncio.sleep(1)
            else:  # 실시간 데이터가 아닌 경우
                try:
                    resp_json = json.loads(received_text)
                    if resp_json['header']['tr_id'] == 'PINGPONG':  # PINGPONG 데이터인 경우
                        await websocket.pong(received_text)  # 웹소켓 클라이언트에서 pong을 보냄
                        logger.debug(f"PINGPONG 데이터 전송: [{received_text}]")
                    else:
                        kis_ws_model = KisWsResponse.from_json_str(received_text)
                        aes_iv = kis_ws_model.body.output.iv if kis_ws_model.body.output.iv is not None else aes_iv
                        aes_key = kis_ws_model.body.output.key if kis_ws_model.body.output.key is not None else aes_key
                        logger.info(f"PINGPONG 아닌 것: [{received_text}]")
                        logger.debug(f"kis_ws_model: {json.dumps(kis_ws_model.model_dump(), ensure_ascii=False)}")
                except ValueError as e:
                    logger.error(f"Error parsing response: {e}")

async def user_input(input_queue):
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        choice = input(timestamp + ": Enter 'exit' to exit or '1' for 주식호가 등록 or '2' for 주식체결 등록: ")
        await input_queue.put(choice)
        if choice == 'exit':
            break

async def run():
    await init_db()
    user_service = get_user_service()
    user = await user_service.get_1("kdy987")
    
    KIS_APP_KEY = user.get_value_by_key("KIS_APP_KEY")
    KIS_APP_SECRET = user.get_value_by_key("KIS_APP_SECRET")
    KIS_HTS_USER_ID = user.get_value_by_key("KIS_HTS_USER_ID")
    kis_ws_url = 'ws://ops.koreainvestment.com:21000'
    custtype = 'P'

    ws_approval_key = await get_ws_approval_key(KIS_APP_KEY, KIS_APP_SECRET)

    print(f"ws access key :[{ws_approval_key}]")

    input_queue = asyncio.Queue()

    while True:
        user_input_task = asyncio.create_task(user_input(input_queue))
        websocket_task = asyncio.create_task(handle_websocket(kis_ws_url, KisWsRequest(
            header=Header(
                approval_key=ws_approval_key,
                personalseckey=KIS_APP_SECRET,
                custtype=custtype,
                tr_type='1'  # 기본값 설정
            ),
            body=Body(
                input=Input(
                    tr_id='H0STASP0',  # 기본값 설정
                    tr_key='005930'
                )
            )
        ), input_queue))

        done, pending = await asyncio.wait(
            [user_input_task, websocket_task],
            return_when=asyncio.FIRST_COMPLETED,
        )

        for task in pending:
            task.cancel()

        choice = await input_queue.get()
        if choice == 'exit':
            break

        stk_code = '005930'
        if choice == '1':  # 주식호가 등록
            tr_id = 'H0STASP0'
            tr_type = '1'
        elif choice == '2':  # 주식체결 등록
            tr_id = 'H0STCNT0'
            tr_type = '1'
        else:
            print('잘못된 입력입니다.')
            continue

        req = KisWsRequest(
            header=Header(
                approval_key=ws_approval_key,
                personalseckey=KIS_APP_SECRET,
                custtype=custtype,
                tr_type=tr_type
            ),
            body=Body(
                input=Input(
                    tr_id=tr_id,
                    tr_key=stk_code
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(run())
