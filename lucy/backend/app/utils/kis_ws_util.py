import json
import requests
from backend.app.domains.stc.kis.model.kis_websocket_model import H0STASP0, H0STCNI0, H0STCNT0, KisWsRealHeader
from backend.app.domains.stc.kis.model.kis_ws_request_model import Body, Header, Input, KisWsRequest
from enum import StrEnum
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64decode
from backend.app.core.logger import get_logger

logger = get_logger(__name__)

class KIS_WSReq(StrEnum):
    BID_ASK = 'H0STASP0'   # 실시간 국내주식 호가
    CONTRACT = 'H0STCNT0'  # 실시간 국내주식 체결
    NOTICE = 'H0STCNI0'    # 실시간 계좌체결발생통보

def is_real_data(txt: str) -> bool:
    return txt[0] == '0' or txt[0] == '1'

def real_data_trid(txt: str) -> str:
    return txt.split('|')[1]

def new_kis_ws_request() -> KisWsRequest:
    return KisWsRequest(
        header=Header(
            approval_key="",
            personalseckey="",
            custtype="P",
            tr_type="",
            content_type="utf-8"
        ),
        body=Body(
            input=Input(
                tr_id="",
                tr_key=""
            )
        )
    )

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
    # logger.debug("웹소켓 접속키 발급 결과 : " + res.text)    
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
    '''KIS로 부터 받은 문자열을 해석해서 KisWsRealHeader, KisWsRealModelBase 객체로 변환해서 리턴'''
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