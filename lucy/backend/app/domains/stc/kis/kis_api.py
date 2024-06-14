# kis_api.py
"""
모듈 설명: 
    - KIS에서 제공하는 API를 사용하기 위한 클래스
주요 기능:
    -   기능을 넣으시오
에러 :
    -  Access Token은 하루 단위로 만료되므로, 만료되면 다시 발급해야 한다.
    - {'rt_cd': '1', 'msg_cd': 'EGW00123', 'msg1': '기간이 만료된 token 입니다.'}
작성자: 김도영
작성일: 07
버전: 1.0
"""
import json
from typing import List
from fastapi import HTTPException
from pydantic import ValidationError
import requests

from backend.app.core.logger import get_logger
from backend.app.domains.stc.kis.model.kis_inquire_balance_model import KisInquireBalance
from backend.app.domains.stc.kis.model.kis_inquire_daily_ccld_model import InquireDailyCcldDto, InquireDailyCcldRequest
from backend.app.domains.stc.kis.model.kis_order_cash_model import KisOrderCash, OrderCancelRequest, OrderCashDto, OrderRvsecnclDto
from backend.app.domains.stc.kis.model.kis_psearch_result_model import PsearchResultDto
from backend.app.domains.stc.kis.model.kis_search_stock_info_model import SearchStockInfoDto
from backend.app.domains.stc.kis.model.kis_psearch_title_model import PsearchTitleDto
from backend.app.domains.user.user_model import KeyValueData, User
from backend.app.core.dependency import get_user_service
from backend.app.domains.user.user_service import UserService
from backend.app.core.exception.lucy_exception import KisAccessTokenExpireException, KisAccessTokenInvalidException
logger = get_logger(__name__)

class KoreaInvestmentApi:
    # _instance = None

    _BASE_URL = 'https://openapi.koreainvestment.com:9443'
    
    def __init__(self, user: User):
        self.user = user
        self.HTS_USER_ID = self.get_key_value(self.user.key_values,"KIS_HTS_USER_ID")
        self.APP_KEY = self.get_key_value(self.user.key_values,"KIS_APP_KEY")
        self.APP_SECRET = self.get_key_value(self.user.key_values,"KIS_APP_SECRET")
        self.ACCTNO = self.get_key_value(self.user.key_values,"KIS_ACCTNO")
        access_token = self.get_key_value(self.user.key_values,"KIS_ACCESS_TOKEN")
        if access_token:
            self.ACCESS_TOKEN = access_token
        else:
            self.set_access_token_from_kis()
    #TODO : 모델 쪽으로 뻴 것을 고려해보자    
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

    def test_access_token(self):
        ''' Access Token 만료 여부 확인 '''
        try:
            cost = self.get_current_price("005930") # 삼성전자
        except KisAccessTokenExpireException as e:
            self.set_access_token_from_kis()

    async def set_access_token_from_kis(self)->str:
        ''' Access Token 발급을 kis 서버로부터 받아서 self에 채우고 users db에 넣는다. '''
        url = f'{self._BASE_URL}/oauth2/tokenP'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        body = {"grant_type":"client_credentials",
                "appkey":self.APP_KEY, 
                "appsecret":self.APP_SECRET}
        res = requests.post(url, headers=headers, data=json.dumps(body))
        
        ACCESS_TOKEN = res.json()["access_token"]
        
        self.ACCESS_TOKEN = ACCESS_TOKEN
        
        logger.debug("----------------------------------------------")
        logger.debug(f"ACCESS_TOKEN : [{ACCESS_TOKEN}]")
        logger.debug("----------------------------------------------")
        self.upsert_key_value(self.user.key_values, "KIS_ACCESS_TOKEN", ACCESS_TOKEN )
        #self.user.key_values["KIS_ACCESS_TOKEN"] = ACCESS_TOKEN
        # db에 저장
        logger.debug(f"self.user : {self.user.to_dict()}")
        user_service = get_user_service()
        await user_service.update_user(self.user.user_id, self.user)
        return ACCESS_TOKEN
    
    def hashkey(self, datas):
        """암호화"""
        url = self.BASE_URL + "/uapi/hashkey" #self._PATHS['암호화']
        headers = {
        'content-Type' : 'application/json',
        'appKey' : self.APP_KEY,
        'appSecret' : self.APP_SECRET
        }
        res = requests.post(url, headers=headers, data=json.dumps(datas))
        hashkey = res.json()["HASH"]
        return hashkey

    def check_access_token(self, json:dict) -> None:
        ''' 토큰 만료 여부 확인 '''
        if json['rt_cd'] == '1' and json['msg_cd'] == 'EGW00123':
            raise KisAccessTokenExpireException("KIS Access Token Expired(접속토큰이 만료됨)")
        if json['rt_cd'] == '1' and json['msg_cd'] == 'EGW00121':
            raise KisAccessTokenInvalidException("KIS Access Token Invalid(접속토큰이 유효하지 않음)")

        return None

    def get_current_price(self, stk_code:str ) ->int:
        ''' 현재가 조회 '''
        url = self._BASE_URL + '/uapi/domestic-stock/v1/quotations/inquire-price' 
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
        json = response.json()
        
        self.check_access_token(json)  

        logger.debug(f"response : {json}")        
        logger.debug(f"현재가: {stk_code} : {json['output']['stck_prpr']}")

        return int(json['output']['stck_prpr'])
        
    def get_inquire_balance(self) ->KisInquireBalance:
        ''' 주식 잔고 조회 '''
        # url = self._PATHS["주식잔고조회"]
        url = self._BASE_URL + "/uapi/domestic-stock/v1/trading/inquire-balance"
        headers = {
            "Content-Type":"application/json", 
            "authorization":f"Bearer {self.ACCESS_TOKEN}",
            "appKey":self.APP_KEY,
            "appSecret":self.APP_SECRET,
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
            self.check_access_token(response.json())  
            raise HTTPException(status_code=response.status_code, detail=f"Error fetching balance: {response.text}")

        try:
            json_data = response.json()
            kis_inquire_balance = KisInquireBalance(**json_data)
        except requests.exceptions.JSONDecodeError:
            logger.error(f"Error decoding JSON: {response.text}")
            raise HTTPException(status_code=500, detail="Invalid JSON response")            
        except ValidationError as e:
            raise HTTPException(status_code=500, detail=f"Error parsing JSON: {e}")

        return kis_inquire_balance


    def order_cash(self,  order_cash : OrderCashDto ) -> KisOrderCash:
        ''' 현금 매수 or 매도 '''
        logger.info(f"현금 매수 매도(order_cash) : {order_cash}")
        url = self._BASE_URL + "/uapi/domestic-stock/v1/trading/order-cash"
        tr_id = "TTTC0802U" if order_cash.buy_sell_gb == "매수" else "TTTC0801U"
        headers = {
            "Content-Type":"application/json", 
            "authorization":f"Bearer {self.ACCESS_TOKEN}",
            "appkey":self.APP_KEY,
            "appsecret":self.APP_SECRET,
            "tr_id":tr_id,
            "custtype":"P"
        }
        if order_cash.cost == 0:
            data = {
                "CANO": self.ACCTNO[0:8],
                "ACNT_PRDT_CD": self.ACCTNO[8:10],
                "PDNO" : order_cash.stk_code,
                "ORD_DVSN" : "01", # 시장가
                "ORD_QTY" : str(order_cash.qty), 
                "ORD_UNPR" : "0" 
            }
        else:
            data = {
                "CANO": self.ACCTNO[0:8],
                "ACNT_PRDT_CD": self.ACCTNO[8:10],
                "PDNO" : order_cash.stk_code,
                "ORD_DVSN" : "00", # 시장가
                "ORD_QTY" : str(order_cash.qty), 
                "ORD_UNPR" : str(order_cash.cost)
            }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        logger.debug(f"response : {response.text}")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f"Error fetching balance: {response.text}")
        try:
            json_data = response.json()
            kis_order_cash = KisOrderCash(**json_data)
            logger.info(f"주문결과 : {kis_order_cash}")
        except requests.exceptions.JSONDecodeError:
            logger.error(f"Error decoding JSON: {response.text}")
            raise HTTPException(status_code=500, detail="Invalid JSON response")
        except ValidationError as e:
            raise HTTPException(status_code=500, detail=f"Error parsing JSON: {e}")
        return kis_order_cash
    
    def search_stock_info(self, stk_code:str) -> SearchStockInfoDto:
        ''' 국내 상품정보 '''
        logger.info(f"상품정보 : {stk_code}")
        url = self._BASE_URL + "/uapi/domestic-stock/v1/quotations/search-stock-info"
        headers ={
            "content-type": "application/json; charset=utf-8",
            'Accept': 'application/json',
            "authorization": f"Bearer {self.ACCESS_TOKEN}",
            "appkey": self.APP_KEY,
            "appsecret": self.APP_SECRET,
            "tr_id": "CTPF1002R",
            "custtype": "P" # B : 법인 P : 개인",
        }        
        data = {
            "PRDT_TYPE_CD": "300", #300 주식, ETF, ETN, ELW 301 : 선물옵션 302 : 채권 306 : ELS'",
            "PDNO" : stk_code
        }
        response = requests.get(url, headers=headers, params=data)
        logger.debug(f"response : {response.text}")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f"Error fetching balance: {response.text}")
        try:
            json_data = response.json()
            stock_info = SearchStockInfoDto(**json_data)
            logger.info(f"상품정보 : {stock_info}")
        except requests.exceptions.JSONDecodeError:
            logger.error(f"Error decoding JSON: {response.text}")
            raise HTTPException(status_code=500, detail="Invalid JSON response")
        except ValidationError as e:
            raise HTTPException(status_code=500, detail=f"Error parsing JSON: {e}")
        return stock_info

    def psearch_title(self) -> PsearchTitleDto:
        ''' 조건식 목록 조회 '''
        logger.info(f"조건식 목록 조회 ")
        url = self._BASE_URL + "/uapi/domestic-stock/v1/quotations/psearch-title"
        data = {
            "user_id": self.HTS_USER_ID
        }        
        headers ={
            "content-type": "application/json; charset=utf-8",
            "authorization": f"Bearer {self.ACCESS_TOKEN}",
            "appkey": self.APP_KEY,
            "appsecret": self.APP_SECRET,
            "tr_id": "HHKST03900300",
            "custtype": "P", # B : 법인 P : 개인",
            "tr_cont" : ""
        }        

        response = requests.get(url, headers=headers, params=data)
        logger.debug(f"response : {response.text}")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f"Error fetching balance: {response.text}")
        try:
            json_data = response.json()
            psearch_title = PsearchTitleDto(**json_data)
            logger.info(f"조건식 목록 조회 : {psearch_title}")
        except requests.exceptions.JSONDecodeError:
            logger.error(f"Error decoding JSON: {response.text}")
            raise HTTPException(status_code=500, detail="Invalid JSON response")
        except ValidationError as e:
            raise HTTPException(status_code=500, detail=f"Error parsing JSON: {e}")
        return psearch_title
    
    def psearch_result(self, seq: str) -> PsearchResultDto:
        ''' 조건식 결과 리스트  '''
        logger.info(f"조건식 결과 조회 ")
        url = self._BASE_URL + "/uapi/domestic-stock/v1/quotations/psearch-result"
        data = {
            "user_id": self.HTS_USER_ID,
            "seq" : seq
        }        
        headers ={
            "content-type": "application/json; charset=utf-8",
            "authorization": f"Bearer {self.ACCESS_TOKEN}",
            "appkey": self.APP_KEY,
            "appsecret": self.APP_SECRET,
            "tr_id": "HHKST03900400",
            "custtype": "P"
        }        

        response = requests.get(url, headers=headers, params=data)
        logger.debug(f"response : {response.text}")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f"Error fetching balance: {response.text}")
        try:
            json_data = response.json()
            psearch_result = PsearchResultDto(**json_data)
            logger.info(f"조건식 목록 조회 : {psearch_result}")
        except requests.exceptions.JSONDecodeError:
            logger.error(f"Error decoding JSON: {response.text}")
            raise HTTPException(status_code=500, detail="Invalid JSON response")
        except ValidationError as e:
            raise HTTPException(status_code=500, detail=f"Error parsing JSON: {e}")
        return psearch_result    

    def inquire_daily_ccld(self, inquire_daily_ccld: InquireDailyCcldRequest) -> InquireDailyCcldDto:
        '''주식일별주문체결조회 '''
        logger.info(f"주식일별주문체결조회")
        url = self._BASE_URL + "/uapi/domestic-stock/v1/trading/inquire-daily-ccld"
        params =  {
            "cano": self.ACCTNO[0:8],
            "acnt_prdt_cd": self.ACCTNO[8:10],
            "inqr_strt_dt": inquire_daily_ccld.inqr_strt_dt,
            "inqr_end_dt": inquire_daily_ccld.inqr_end_dt,
            "sll_buy_dvsn_cd": inquire_daily_ccld.sll_buy_dvsn_cd, # 00 : 전체, 01 : 매도, 02 : 매수",
            "inqr_dvsn": inquire_daily_ccld.inqr_dvsn,   # 00 : 역순 01 : 정순",
            "pdno": inquire_daily_ccld.pdno,
            "ccld_dvsn": inquire_daily_ccld.ccld_dvsn, #00 : 전체 01 : 체결 02 : 미체결",
            "ord_gno_brno": "",
            "odno": "",
            "inqr_dvsn_3": inquire_daily_ccld.inqr_dvsn_3, # 00 : 전체 01 : 현금 02 : 융자 03 : 대출 04 : 대주",
            "inqr_dvsn_1": "", # 공란 : 전체 1 : ELW 2 : 프리보드",
            "ctx_area_fk100": inquire_daily_ccld.CTX_AREA_FK100, #"란 : 최초 조회시 이전 조회 Output CTX_AREA_FK100 값 : 다음페이지 조회시(2번째부터)",
            "ctx_area_nk100": inquire_daily_ccld.CTX_AREA_NK100  #공란 : 최초 조회시 이전 조회 Output CTX_AREA_NK100 값 : 다음페이지 조회시(2번째부터)",
        }   
        headers ={
            "authorization": f"Bearer {self.ACCESS_TOKEN}",
            "appkey": self.APP_KEY,
            "appsecret": self.APP_SECRET,
            "tr_id": "TTTC8001R" # TTTC8001R: 주식 일별 주문 체결 조회(3개월이내) CTSC9115R : 주식 일별 주문 체결 조회(3개월이전)
        }        

        response = requests.get(url, headers=headers, params=params)
        logger.debug(f"response : {response.text}")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f"Error 주식일별주문체결조회 : {response.text}")
        try:
            json_data = response.json()
            inquire_daily_ccld = InquireDailyCcldDto(**json_data)
            logger.debug(f"주식일별주문체결조회 됨")
        except requests.exceptions.JSONDecodeError:
            logger.error(f"Error decoding JSON: {response.text}")
            raise HTTPException(status_code=500, detail="Invalid JSON response")
        except ValidationError as e:
            raise HTTPException(status_code=500, detail=f"Error parsing JSON: {e}")
        return inquire_daily_ccld    
    
    def order_cancel(self, order_cancel: OrderCancelRequest) -> OrderRvsecnclDto:
        '''주식 주문 취소 '''
        logger.info(f"주식 주문 취소")
        url = self._BASE_URL + "/uapi/domestic-stock/v1/trading/order-rvsecncl"
        body =  {
            "CANO": self.ACCTNO[0:8],
            "ACNT_PRDT_CD": self.ACCTNO[8:10],
            "KRX_FWDG_ORD_ORGNO": "",  # (Null 값 설정) 주문시 한국투자증권 시스템에서 지정된 영업점코드",
            "ORGN_ODNO": order_cancel.orgn_odno,   #"주식일별주문체결조회 API output1의 odno(주문번호) 값 입력 주문시 한국투자증권 시스템에서 채번된 주문번호",
            "ORD_DVSN": order_cancel.ord_dvsn_cd, #"00 : 지정가 01 : 시장가 02 : 조건부지정가 03 : 최유리지정가 04 : 최우선지정가 05 : 장전 시간외 06 : 장후 시간외 07 : 시간외 단일가 08 : 자기주식 09 : 자기주식S-Option 10 : 자기주식금전신탁 11 : IOC지정가 (즉시체결,잔량취소) 12 : FOK지정가 (즉시체결,전량취소) 13 : IOC시장가 (즉시체결,잔량취소) 14 : FOK시장가 (즉시체결,전량취소) 15 : IOC최유리 (즉시체결,잔량취소) 16 : FOK최유리 (즉시체결,전량취소)",
            "RVSE_CNCL_DVSN_CD": "02", #정정 : 01 취소 : 02",
            "ORD_QTY": "0", # [잔량전부 취소/정정주문] "0" 설정 ( QTY_ALL_ORD_YN=Y 설정 ) [잔량일부 취소/정정주문] 취소/정정 수량",
            "ORD_UNPR": "0",  #[정정] (지정가) 정정주문 1주당 가격 (시장가) "0" 설정 [취소] "0" 설정",
            "QTY_ALL_ORD_YN": "Y" #[정정/취소] Y : 잔량전부 N : 잔량일부",
        }   
        headers ={
            "authorization": f"Bearer {self.ACCESS_TOKEN}",
            "appkey": self.APP_KEY,
            "appsecret": self.APP_SECRET,
            "tr_id": "TTTC0803U" #[실전투자] TTTC0803U : 주식 정정 취소 주문 [모의투자] VTTC0803U : 주식 정정 취소 주문",                        
        }        

        response = requests.get(url, headers=headers, data=json.dumps(body))
        logger.debug(f"response : {response.text}")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f"Error 주식일별주문체결조회 : {response.text}")
        try:
            json_data = response.json()
            order_cancel = OrderRvsecnclDto(**json_data)
            logger.debug(f"주식 주문 잔량 전부 취소 됨")
        except requests.exceptions.JSONDecodeError:
            logger.error(f"Error decoding JSON: {response.text}")
            raise HTTPException(status_code=500, detail="Invalid JSON response")
        except ValidationError as e:
            raise HTTPException(status_code=500, detail=f"Error parsing JSON: {e}")
        return order_cancel  