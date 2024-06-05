import json
from typing import List
from fastapi import HTTPException
from pydantic import ValidationError
import requests

from backend.app.core.logger import get_logger
from backend.app.domains.stc.kis.kis_inquire_balance_model import KisInquireBalance
from backend.app.domains.user.user_model import KeyValueData, User
from backend.app.core.dependency import get_user_service
from backend.app.domains.user.user_service import UserService
logger = get_logger(__name__)

class KoreaInvestmentApi:
    # _instance = None

    _BASE_URL = 'https://openapi.koreainvestment.com:9443'
    _PATHS = {
        "토큰발급" : f'{_BASE_URL}/oauth2/tokenP',
        "암호화" : f'{_BASE_URL}/uapi/hashkey',
        "현재가조회" : f'{_BASE_URL}/uapi/domestic-stock/v1/quotations/inquire-price',
        "주식잔고조회" : f'{_BASE_URL}/uapi/domestic-stock/v1/quotations/inquire-stock-balance',
    }
    
    def __init__(self, user: User):
        self.user = user
        self.APP_KEY = self.get_key_value(self.user.key_values,"KIS_APP_KEY")
        self.APP_SECRET = self.get_key_value(self.user.key_values,"KIS_APP_SECRET")
        self.ACCTNO = self.get_key_value(self.user.key_values,"KIS_ACCTNO")
        access_token = self.get_key_value(self.user.key_values,"KIS_ACCESS_TOKEN")
        if access_token:
            self.ACCESS_TOKEN = access_token
        else:
            self.set_access_token()
    
    def get_key_value(self, key_values:List[KeyValueData], key_name:str) -> str:
        for item in key_values:
            if item.key == key_name:
                return item.value
        return ''
    def upsert_key_value(self, key_values: List[KeyValueData], key_name: str, key_value: str):
        for item in key_values:
            if item.key == key_name:
                item.value = key_value
                return
        # 키 값이 없으면 새로운 항목 추가
        key_values.append(KeyValueData(key=key_name, value=key_value))

    def set_access_token(self):
        ''' Access Token 발급을 kis 서버로부터 받아서 self에 채우고 users db에 넣는다. '''
        url = self._PATHS['토큰발급']
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        body = {"grant_type":"client_credentials",
                "appkey":self.APP_KEY, 
                "appsecret":self.APP_SECRET}
        res = requests.post(url, headers=headers, data=json.dumps(body))
        ACCESS_TOKEN = res.json()["access_token"]
        logger.debug("----------------------------------------------")
        logger.debug(f"ACCESS_TOKEN : [{ACCESS_TOKEN}]")
        logger.debug("----------------------------------------------")
        self.upsert_key_value(self.user.key_values, "KIS_ACCESS_TOKEN", ACCESS_TOKEN )
        #self.user.key_values["KIS_ACCESS_TOKEN"] = ACCESS_TOKEN
        # db에 저장
        get_user_service().update_user(self.user.user_id, self.user)

    def hashkey(self, datas):
        """암호화"""
        url = self._PATHS['암호화']
        headers = {
        'content-Type' : 'application/json',
        'appKey' : self.APP_KEY,
        'appSecret' : self.APP_SECRET
        }
        res = requests.post(url, headers=headers, data=json.dumps(datas))
        hashkey = res.json()["HASH"]
        return hashkey

    def get_current_price(self, stk_code:str ) ->int:
        ''' 현재가 조회 '''
        url = self._PATHS["현재가조회"]
        headers = {"Content-Type":"application/json", 
                "authorization": f"Bearer {self.ACCESS_TOKEN}",
                "appKey":self.APP_KEY,
                "appSecret":self.APP_SECRET,
                "tr_id":"FHKST01010100"}
        params = {
            "fid_cond_mrkt_div_code":"J",
            "fid_input_iscd":stk_code,
        }
        response = requests.get(url, headers=headers, params=params)
        logger.debug(f"response : {response.json()}")
        json = response.json()
        logger.debug(f"현재가: {stk_code} : {json['output']['stck_prpr']}")
        #return json['output']['stck_prpr']
        return int(json['output']['stck_prpr'])
    
    def get_balance(self) ->KisInquireBalance:
        ''' 주식 잔고 조회 '''
        # url = self._PATHS["주식잔고조회"]
        url = self._BASE_URL + "/uapi/domestic-stock/v1/trading/inquire-balance"
        headers = {"Content-Type":"application/json", 
            "authorization":f"Bearer {self.ACCESS_TOKEN}",
            "appKey":self.APP_KEY,
            "appSecret":self.APP_SECRET,
            # "tr_id":"TTTC8908R",
            "tr_id":"TTTC8434R"
        }
        CANO = self.ACCTNO[0:8]
        ACNT_PRDT_CD = self.ACCTNO[8:10]
        params = {
            "CANO": CANO,
            "ACNT_PRDT_CD": ACNT_PRDT_CD,
            "AFHR_FLPR_YN": "N",
            "OFL_YN": "N",
            "INQR_DVSN": "01",
            "UNPR_DVSN": "01",
            "FUND_STTL_ICLD_YN": "N",
            "FNCG_AMT_AUTO_RDPT_YN": "N",
            "PRCS_DVSN": "01",
            "CTX_AREA_FK100": "",
            "CTX_AREA_NK100": ""
        }
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f"Error fetching balance: {response.text}")

        try:
            json = response.json()
            kis_inquire_balance = KisInquireBalance(**json)
        except requests.exceptions.JSONDecodeError:
            logger.error(f"Error decoding JSON: {response.text}")
            raise HTTPException(status_code=500, detail="Invalid JSON response")            
        except ValidationError as e:
            raise HTTPException(status_code=500, detail=f"Error parsing JSON: {e}")

        return kis_inquire_balance

    # def get_stock_balance(self, headers:dict,  param: dict ) ->dict:
    #     ''' 주식 잔고 조회 '''
    #     url = self._PATHS["주식잔고조회"]
    #     response = requests.get(url, headers=headers, params=param)
    #     logger.debug(f"response : {response.json()}")
    #     return response.json()