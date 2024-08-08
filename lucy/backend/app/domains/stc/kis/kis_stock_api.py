# kis_stock_api.py
"""
모듈 설명: 
    - KIS에서 제공하는 API를 사용하기 위한 클래스
주요 기능:
/oauth2/tokenP
/uapi/hashkey
/uapi/domestic-stock/v1/quotations/inquire-price 
/uapi/domestic-stock/v1/trading/inquire-balance
/uapi/domestic-stock/v1/trading/order-cash - 
/uapi/domestic-stock/v1/quotations/search-stock-info
/uapi/domestic-stock/v1/quotations/psearch-title
/uapi/domestic-stock/v1/quotations/psearch-result
/uapi/domestic-stock/v1/trading/inquire-daily-ccld
/uapi/domestic-stock/v1/trading/order-rvsecncl
/uapi/domestic-stock/v1/trading/inquire-psbl-rvsecncl
/uapi/domestic-stock/v1/trading/inquire-psbl-order #매수가능조회
/uapi/domestic-stock/v1/trading/inquire-psbl-sell  #매도가능조회
/uapi/domestic-stock/v1/quotations/chk-holiday
에러 :
    -  Access Token은 하루 단위로 만료되므로, 만료되면 다시 발급해야 한다.
    - {'rt_cd': '1', 'msg_cd': 'EGW00123', 'msg1': '기간이 만료된 token 입니다.'}
작성자: 김도영
작성일: 07
버전: 1.0
"""
import asyncio
from datetime import datetime, timedelta
import json
import aiohttp
from fastapi import HTTPException
import requests
from pydantic import ValidationError

from backend.app.core.logger import get_logger
from backend.app.domains.stc.kis.model.kis_after_hour_balance_model import AfterHourBalance_Request, AfterHourBalance_Response
from backend.app.domains.stc.kis.model.kis_chk_holiday_model import ChkWorkingDay_Response
from backend.app.domains.stc.kis.model.kis_inquire_balance_model import KisInquireBalance_Response
from backend.app.domains.stc.kis.model.kis_inquire_daily_ccld_model import InquireDailyCcld_Response, InquireDailyCcld_Request
from backend.app.domains.stc.kis.model.kis_inquire_price import InquirePrice_Response
from backend.app.domains.stc.kis.model.kis_inquire_psbl_rvsecncl_model import InquirePsblRvsecncl_Response
from backend.app.domains.stc.kis.model.kis_inquire_psbl_sell_model import InquirePsblSell_Response
from backend.app.domains.stc.kis.model.kis_inquire_psble_order import InquirePsblOrder_Response, InquirePsblOrder_Request
from backend.app.domains.stc.kis.model.kis_order_cash_model import KisOrderRvsecncl_Request, OrderCash_Request, KisOrderCash_Response, KisOrderCancel_Response
from backend.app.domains.stc.kis.model.kis_psearch_result_model import PsearchResult_Response
from backend.app.domains.stc.kis.model.kis_quote_balance_model import QuoteBalance_Request, QuoteBalance_Response
from backend.app.domains.stc.kis.model.kis_search_stock_info_model import SearchStockInfo_Response
from backend.app.domains.stc.kis.model.kis_psearch_title_model import PsearchTitle_Result
from backend.app.domains.stc.stock_api import StockApi
from backend.app.domains.user.user_model import StkAccount, User
from backend.app.core.exception.lucy_exception import AccessTokenExpireException, AccessTokenInvalidException, InvalidResponseException, KisApiException

logger = get_logger(__name__)

class KisStockApi(StockApi):
    
    def __init__(self, user:User, account: StkAccount):
        super().__init__(user.user_id, account.account_no)
        self.user = user
        self.account = account
        self.BASE_URL ='https://openapi.koreainvestment.com:9443'
        self.HTS_USER_ID = account.get_value('KIS_HTS_USER_ID')
        self.APP_KEY = account.get_value('KIS_APP_KEY')
        self.APP_SECRET = account.get_value('KIS_APP_SECRET')
        self.ACCTNO = account.account_no
        self.ACCESS_TOKEN = None
        self.ACCESS_TOKEN_TIME = None
        access_token = account.get_value('KIS_ACCESS_TOKEN')
        if access_token:
            self.ACCESS_TOKEN = access_token
            self.ACCESS_TOKEN_TIME = account.get_value('KIS_ACCESS_TOKEN_TIME')
        self.last_request_time = None    

    def get_access_token_time(self)->datetime:
        if self.ACCESS_TOKEN_TIME:
            return datetime.strptime(self.ACCESS_TOKEN_TIME, "%Y-%m-%d %H:%M:%S")
        else:
            return None
        
    def is_token_expired(self) -> bool:
        token_time = self.get_access_token_time()
        if token_time and datetime.now() > token_time + timedelta(hours=23):
            return True
        return False        
        
    async def initialize(self) -> bool:
        ''' Access Token 존재여부 및  만료 여부 확인 '''

        # 토큰이 없거나 만료되었는지 확인
        if self.ACCESS_TOKEN is None or self.is_token_expired():
            logger.info("KIS API Access Token이 없거나 만료되었습니다. 새로 발급합니다.")
            await self.set_access_token_from_kis()

        # 만료여부 체크
        try:
            cost = await self.get_current_price("005930") # 삼성전자
        except AccessTokenExpireException as e:
            logger.info("KIS API Access Token이 유효하지 않습니다. 새로 발급합니다.")
            await self.set_access_token_from_kis()

        return True    

    async def set_access_token_from_kis(self)->str:
        ''' 동기 방식으로 Access Token 발급을 KIS 서버로부터 받아서 self에 채우고 users db에 넣는다. '''
        # 1분 제한 체크
        if self.last_request_time and datetime.now() - self.last_request_time < timedelta(minutes=1):
            time_to_sleep = 60 - (datetime.now() - self.last_request_time).seconds
            logger.debug(f"Sleeping for {time_to_sleep} seconds due to rate limiting")
            asyncio.sleep(time_to_sleep)

        self.last_request_time = datetime.now()

        url = f'{self.BASE_URL}/oauth2/tokenP'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        body = { 
            "grant_type": "client_credentials",
            "appkey": self.APP_KEY,
            "appsecret": self.APP_SECRET
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(body))
            response.raise_for_status()  # HTTP 에러가 발생하면 예외 발생

            response_json = response.json()

            self.ACCESS_TOKEN = response_json['access_token']
            self.ACCESS_TOKEN_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            logger.debug("----------------------------------------------")
            logger.debug(f"ACCESS_TOKEN : [{self.ACCESS_TOKEN}]")
            logger.debug("----------------------------------------------")

            self.account.set_value('KIS_ACCESS_TOKEN', self.ACCESS_TOKEN)
            self.account.set_value('KIS_ACCESS_TOKEN_TIME', self.ACCESS_TOKEN_TIME)
            await self.user_service.update_user(self.user.user_id, self.user)
            return self.ACCESS_TOKEN
        except requests.exceptions.RequestException as e:
            logger.error(f"KIS API Access Token 발급 실패: {str(e)}")
            raise KisApiException(f"KIS API Access Token 발급 실패: {str(e)}")
    
    async def hashkey(self, datas):
        """암호화 (동기 함수)"""
        url = self.BASE_URL + "/uapi/hashkey"
        headers = {
            'Content-Type': 'application/json',
            'appKey': self.APP_KEY,
            'appSecret': self.APP_SECRET
        }
        response = requests.post(url, headers=headers, json=datas)
        response_json = response.json()
        hashkey = response_json["HASH"]
        return hashkey
            
    def check_access_token(self, json:dict) -> None:
        ''' 토큰 만료 여부 확인 '''
        if json['rt_cd'] == '1' and json['msg_cd'] == 'EGW00123':
            raise AccessTokenExpireException("KIS Access Token Expired(접속토큰이 만료됨)")
        if json['rt_cd'] == '1' and json['msg_cd'] == 'EGW00121':
            raise AccessTokenInvalidException("KIS Access Token Invalid(접속토큰이 유효하지 않음)")

        return None

    async def send_request(self, title, method, url, headers, params=None, data=None):
        try:
            async with aiohttp.ClientSession() as session:
                if method == 'GET':
                    async with session.get(url, headers=headers, params=params) as response:
                        response.raise_for_status()
                        return await response.json()
                elif method == 'POST':
                    async with session.post(url, headers=headers, data=data) as response:
                        response.raise_for_status()
                        return await response.json()
        except aiohttp.ClientError as e:
            logger.error(f"HTTP 오류 ({title}): {e}")
            raise KisApiException(status_code=500, detail=f"HTTP 오류 ({title}): {e}")                    
        except json.JSONDecodeError as e:
            logger.error(f"Response is not in JSON format.{title}")
            raise InvalidResponseException(f"응답 내용이 JSON형식이 아닙니다 ({title})")

    async def current_cost(self, stk_code:str) -> InquirePrice_Response:
        ''' 현재가 조회 '''
        url = self.BASE_URL +  '/uapi/domestic-stock/v1/quotations/inquire-price' 
        headers = {"Content-Type":"application/json", 
                "authorization": f"Bearer {self.ACCESS_TOKEN}",
                "appKey":self.APP_KEY,
                "appSecret":self.APP_SECRET,
                "tr_id":"FHKST01010100"}
        params = {
            "fid_cond_mrkt_div_code":"J",
            "fid_input_iscd":stk_code,
        }
        json_response = await self.send_request('현재가 조회', 'GET', url, headers, params=params)
        self.check_access_token(json_response)
        logger.debug(f"현재가: {stk_code} : {json_response['output']['stck_prpr']}")
        try:
            return InquirePrice_Response(**json_response)
        except ValidationError as e:
            raise HTTPException(status_code=500, detail=f"받은 json 파싱 오류: {e}")        


    async def get_current_price(self, stk_code: str) -> int:
        ''' 현재가 조회 '''
        url = self.BASE_URL + '/uapi/domestic-stock/v1/quotations/inquire-price'
        headers = {
            "Content-Type": "application/json",
            "authorization": f"Bearer {self.ACCESS_TOKEN}",
            "appKey": self.APP_KEY,
            "appSecret": self.APP_SECRET,
            "tr_id": "FHKST01010100"
        }
        params = {
            "fid_cond_mrkt_div_code": "J",
            "fid_input_iscd": stk_code,
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                try:
                    json_response = await response.json()
                except aiohttp.ClientError as e:
                    logger.error(f"API 요청 실패: {e}")
                    raise KisApiException(f"API 요청 실패: {e}")
                except json.JSONDecodeError:
                    logger.error("응답이 JSON 형식이 아닙니다.")
                    raise InvalidResponseException("응답이 JSON 형식이 아닙니다.")

                # Access token 체크
                self.check_access_token(json_response)

                # 'output' 키가 있는지 확인
                if 'output' not in json_response:
                    logger.error(f"응답에 'output' 키가 없습니다: {json_response}")
                    raise InvalidResponseException("응답에 'output' 키가 없습니다.")

                try:
                    current_price = int(json_response['output']['stck_prpr'])
                    logger.debug(f"현재가: {stk_code} : {current_price}")
                    return current_price
                except KeyError:
                    logger.error(f"응답에 'stck_prpr' 키가 없습니다: {json_response}")
                    raise InvalidResponseException("응답에 'stck_prpr' 키가 없습니다.")
                except ValueError:
                    logger.error(f"'stck_prpr' 값을 정수로 변환할 수 없습니다: {json_response['output']['stck_prpr']}")
                    raise InvalidResponseException("'stck_prpr' 값을 정수로 변환할 수 없습니다.")

    async def order(self, order_cash : OrderCash_Request ) -> KisOrderCash_Response:
        ''' 현금 매수/매도 '''
        logger.info(f"현금 매수 매도(order_cash) : {order_cash}")

        url = self.BASE_URL + "/uapi/domestic-stock/v1/trading/order-cash"
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
                "ORD_DVSN" : "00", 
                "ORD_QTY" : str(order_cash.qty), 
                "ORD_UNPR" : str(order_cash.cost)
            }
        json_response = await self.send_request('현금 매수/매도', 'POST', url, headers, data=json.dumps(data))
        try:
            return KisOrderCash_Response(**json_response)
        except ValidationError as e:
            raise HTTPException(status_code=500, detail=f"Error parsing JSON: {e}")        

    async def order_cancel(self, org_order_no: str) -> KisOrderCancel_Response:
        '''주식 주문 취소 '''
        logger.info(f"주식 주문 취소")
        url = self.BASE_URL + "/uapi/domestic-stock/v1/trading/order-rvsecncl"
        body =  {
            "CANO": self.ACCTNO[0:8],
            "ACNT_PRDT_CD": self.ACCTNO[8:10],
            "KRX_FWDG_ORD_ORGNO": "",  # (Null 값 설정) 주문시 한국투자증권 시스템에서 지정된 영업점코드",
            "ORGN_ODNO": org_order_no,   #"주식일별주문체결조회 API output1의 odno(주문번호) 값 입력 주문시 한국투자증권 시스템에서 채번된 주문번호",
            "ORD_DVSN": "00", #"00 : 지정가 01 : 시장가 02 : 조건부지정가 03 : 최유리지정가 04 : 최우선지정가 05 : 장전 시간외 06 : 장후 시간외 07 : 시간외 단일가 08 : 자기주식 09 : 자기주식S-Option 10 : 자기주식금전신탁 11 : IOC지정가 (즉시체결,잔량취소) 12 : FOK지정가 (즉시체결,전량취소) 13 : IOC시장가 (즉시체결,잔량취소) 14 : FOK시장가 (즉시체결,전량취소) 15 : IOC최유리 (즉시체결,잔량취소) 16 : FOK최유리 (즉시체결,전량취소)",
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
        json_response = await self.send_request('주식 주문취소', 'POST', url, headers=headers, data=json.dumps(body))
        try:
            return KisOrderCancel_Response(**json_response)
        except ValidationError as e:
            raise HTTPException(status_code=500, detail=f"Error parsing JSON: {e}")

    async def order_modify(self, req: KisOrderRvsecncl_Request) -> KisOrderCancel_Response:
        '''주식 주문 정정 '''
        logger.info(f"주식 주문 정정")
        url = self.BASE_URL + "/uapi/domestic-stock/v1/trading/order-rvsecncl"
        body =  {
            "CANO": self.ACCTNO[0:8],
            "ACNT_PRDT_CD": self.ACCTNO[8:10],
            "KRX_FWDG_ORD_ORGNO": "",  # (Null 값 설정) 주문시 한국투자증권 시스템에서 지정된 영업점코드",
            "ORGN_ODNO": req.ORGN_ODNO,   #"주식일별주문체결조회 API output1의 odno(주문번호) 값 입력 주문시 한국투자증권 시스템에서 채번된 주문번호",
            "ORD_DVSN": req.ORD_DVSN, #"00 : 지정가 01 : 시장가 02 : 조건부지정가 03 : 최유리지정가 04 : 최우선지정가 05 : 장전 시간외 06 : 장후 시간외 07 : 시간외 단일가 08 : 자기주식 09 : 자기주식S-Option 10 : 자기주식금전신탁 11 : IOC지정가 (즉시체결,잔량취소) 12 : FOK지정가 (즉시체결,전량취소) 13 : IOC시장가 (즉시체결,잔량취소) 14 : FOK시장가 (즉시체결,전량취소) 15 : IOC최유리 (즉시체결,잔량취소) 16 : FOK최유리 (즉시체결,전량취소)",
            "RVSE_CNCL_DVSN_CD": "01", #정정 : 01 취소 : 02",
            "ORD_QTY": req.ORD_QTY, # [잔량전부 취소/정정주문] "0" 설정 ( QTY_ALL_ORD_YN=Y 설정 ) [잔량일부 취소/정정주문] 취소/정정 수량",
            "ORD_UNPR": req.ORD_UNPR,  #[정정] (지정가) 정정주문 1주당 가격 (시장가) "0" 설정 [취소] "0" 설정",
            "QTY_ALL_ORD_YN": "N" #[정정/취소] Y : 잔량전부 N : 잔량일부",
        }   
        headers ={
            "authorization": f"Bearer {self.ACCESS_TOKEN}",
            "appkey": self.APP_KEY,
            "appsecret": self.APP_SECRET,
            "tr_id": "TTTC0803U" #[실전투자] TTTC0803U : 주식 정정 취소 주문 [모의투자] VTTC0803U : 주식 정정 취소 주문",                        
        }        

        json_response = await self.send_request('주식 주문 정정','POST', url, headers, data=json.dumps(body))
        try:
            return KisOrderCancel_Response(**json_response)
        except ValidationError as e:
            raise HTTPException(status_code=500, detail=f"Error parsing JSON: {e}")

    async def search_stock_info(self, stk_code:str) -> SearchStockInfo_Response:
        ''' 국내 상품정보 '''
        logger.info(f"상품정보 : {stk_code}")
        url = self.BASE_URL + "/uapi/domestic-stock/v1/quotations/search-stock-info"
        headers ={
            "content-type": "application/json; charset=utf-8",
            'Accept': 'application/json',
            "authorization": f"Bearer {self.ACCESS_TOKEN}",
            "appkey": self.APP_KEY,
            "appsecret": self.APP_SECRET,
            "tr_id": "CTPF1002R",
            "custtype": "P" # B : 법인 P : 개인",
        }        
        params = {
            "PRDT_TYPE_CD": "300", #300 주식, ETF, ETN, ELW 301 : 선물옵션 302 : 채권 306 : ELS'",
            "PDNO" : stk_code
        }
        json_response = await self.send_request('국내 상품정보', 'GET', url, headers, params=params)
        try:
            return SearchStockInfo_Response(**json_response)
        except ValidationError as e:
            raise HTTPException(status_code=500, detail=f"Error parsing JSON: {e}")
        
    async def inquire_balance(self) ->KisInquireBalance_Response:
        ''' 주식 잔고 조회 '''
        url = self.BASE_URL + "/uapi/domestic-stock/v1/trading/inquire-balance"
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
        json_response = await self.send_request('주식 잔고 조회', 'GET', url, headers, params=params)
        try:
            return KisInquireBalance_Response(**json_response)
        except ValidationError as e:
            raise HTTPException(status_code=500, detail=f"Error parsing JSON: {e}")

    async def psearch_title(self) -> PsearchTitle_Result:
        ''' 조건식 목록 조회 '''
        logger.info(f"조건식 목록 조회 ")
        url = self.BASE_URL + "/uapi/domestic-stock/v1/quotations/psearch-title"
        params = {
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
        json_response = await self.send_request('조건식 목록 조회', 'GET', url, headers, params=params)
        try:
            return PsearchTitle_Result(**json_response)
        except ValidationError as e:
            raise HTTPException(status_code=500, detail=f"Error parsing JSON: {e}")
    
    async def psearch_result(self, seq: str) -> PsearchResult_Response:
        ''' 조건식 결과 리스트  '''
        logger.info(f"조건식 결과 리스트 조회 ")
        url = self.BASE_URL + "/uapi/domestic-stock/v1/quotations/psearch-result"
        params = {
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
        json_response = await self.send_request('조건식 결과 리스트', 'GET', url, headers, params=params)
        try:
            return PsearchResult_Response(**json_response)
        except ValidationError as e:
            raise HTTPException(status_code=500, detail=f"Error parsing JSON: {e}")

    async def inquire_daily_ccld(self, inquire_daily_ccld: InquireDailyCcld_Request) -> InquireDailyCcld_Response:
        '''주식일별주문체결조회 '''
        logger.info(f"주식일별주문체결조회")
        url = self.BASE_URL + "/uapi/domestic-stock/v1/trading/inquire-daily-ccld"
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
        json_response = await self.send_request('주식일별주문체결조회','GET', url, headers, params=params)
        try:
            return InquireDailyCcld_Response(**json_response)
        except ValidationError as e:
            raise HTTPException(status_code=500, detail=f"Error parsing JSON: {e}")
    
    ##############################################################################################
    # [국내주식] 주문/계좌 > 주식정정취소가능주문조회[v1_국내주식-004]
    ##############################################################################################
    #주식주문(정정취소) 호출 전에 반드시 주식정정취소가능주문조회 호출을 통해 
    #정정취소가능수량(output > psbl_qty)을 확인하신 후 정정취소주문 내시기 바랍니다.
    async def inquire_psbl_rvsecncl(self) -> InquirePsblRvsecncl_Response:
        '''정정취소 가능수량 조회 '''
        logger.info(f"정정취소 가능수량 조회")
        url = self.BASE_URL + "/uapi/domestic-stock/v1/trading/inquire-psbl-rvsecncl"
        params = {
            "CANO": self.ACCTNO[0:8],
            "ACNT_PRDT_CD": self.ACCTNO[8:10],
            "CTX_AREA_FK100": "",  #공란 : 최초 조회시 이전 조회 Output CTX_AREA_FK100 값 : 다음페이지 조회시(2번째부터)",
            "CTX_AREA_NK100": "",  #공란 : 최초 조회시 이전 조회 Output CTX_AREA_NK100 값 : 다음페이지 조회시(2번째부터)",
            "INQR_DVSN_1": "0",  #0 : 조회순서 1 : 주문순 2 : 종목순",
            "INQR_DVSN_2": "0"  #0 : 전체 1 : 매도 2 : 매수",
        }    
        headers ={
            "authorization": f"Bearer {self.ACCESS_TOKEN}",
            "appkey": self.APP_KEY,
            "appsecret": self.APP_SECRET,
            "tr_id":  "TTTC8036R" #모의투자 사용 불가", 
        }
        json_response = await self.send_request('정정취소 가능수량 조회', 'GET', url, headers, params=params)
        try:
            return InquirePsblRvsecncl_Response(**json_response)
        except ValidationError as e:
            raise HTTPException(status_code=500, detail=f"Error parsing JSON: {e}")

    ##############################################################################################
    # [국내주식] 주문/계좌 > 매수가능조회
    #############################################################################################
    async def inquire_psbl_order(self, ipo_req :InquirePsblOrder_Request ) -> InquirePsblOrder_Response:
        '''매수가능조회 '''
        logger.info(f"매수가능조회")
        url = self.BASE_URL + "/uapi/domestic-stock/v1/trading/inquire-psbl-order"
        params = {
            "CANO": self.ACCTNO[0:8],
            "ACNT_PRDT_CD": self.ACCTNO[8:10],
            "PDNO": ipo_req.pdno, # 종목번호(6자리) * PDNO, ORD_UNPR 공란 입력 시, 매수수량 없이 매수금액만 조회됨
            "ORD_UNPR": ipo_req.ord_unpr, # 1주당 가격 * 시장가(ORD_DVSN:01)로 조회 시, 공란으로 입력 * PDNO, ORD_UNPR 공란 입력 시, 매수수량 없이 매수금액만 조회됨
            "ORD_DVSN": ipo_req.ord_dvsn,  #특정 종목 전량매수 시 가능수량을 확인할 경우  00:지정가는 증거금율이 반영되지 않으므로  증거금율이 반영되는 01: 시장가로 조회 * 다만, 조건부지정가 등 특정 주문구분(ex.IOC)으로 주문 시 가능수량을 확인할 경우 주문 시와 동일한 주문구분(ex.IOC) 입력하여 가능수량 확인 * 종목별 매수가능수량 조회 없이 매수금액만 조회하고자 할 경우 임의값(00) 입력 00 : 지정가 01 : 시장가 02 : 조건부지정가 03 : 최유리지정가 04 : 최우선지정가 05 : 장전 시간외 06 : 장후 시간외 07 : 시간외 단일가 08 : 자기주식 09 : 자기주식S-Option 10 : 자기주식금전신탁 11 : IOC지정가 (즉시체결,잔량취소) 12 : FOK지정가 (즉시체결,전량취소) 13 : IOC시장가 (즉시체결,잔량취소) 14 : FOK시장가 (즉시체결,전량취소) 15 : IOC최유리 (즉시체결,잔량취소) 16 : FOK최유리 (즉시체결,전량취소) 51 : 장중대량 52 : 장중바스켓 62 : 장개시전 시간외대량 63 : 장개시전 시간외바스켓 67 : 장개시전 금전신탁자사주 69 : 장개시전 자기주식 72 : 시간외대량 77 : 시간외자사주신탁 79 : 시간외대량자기주식 80 : 바스켓
            "CMA_EVLU_AMT_ICLD_YN": ipo_req.cma_evlu_amt_icld_yn, #Y : 포함 N : 포함하지 않음
            "OVRS_ICLD_YN": ipo_req.ovrs_icld_yn #Y : 포함 N : 포함하지 않음
        }    
        headers ={
            "authorization": f"Bearer {self.ACCESS_TOKEN}",
            "appkey": self.APP_KEY,
            "appsecret": self.APP_SECRET,
            "tr_id":  "TTTC8908R" #매수가능조회
        }
        json_response = await self.send_request('매수가능조회', 'GET', url, headers, params=params)
        try:
            return InquirePsblOrder_Response(**json_response)
        except ValidationError as e:
            raise HTTPException(status_code=500, detail=f"Error parsing JSON: {e}")

    ##############################################################################################
    # [국내주식] 주문계좌 > 매도가능수량
    # [0971] 주식 매도 화면에서 종목코드 입력 후 "가능" 클릭 시 매도가능수량이 확인되는 기능을 API로 개발한 사항
    # output > ord_psbl_qty(주문가능수량) 확인하실 수 있습니다.
    ##############################################################################################
    async def inquire_psbl_sell(self, stk_code:str) -> InquirePsblSell_Response:
        '''매도가능수량 조회 '''
        logger.info(f"매도가능수량 조회")

        url = self.BASE_URL + "/uapi/domestic-stock/v1/trading/inquire-psbl-sell"

        params = {
            "CANO": self.ACCTNO[0:8],
            "ACNT_PRDT_CD": self.ACCTNO[8:10],
            "PDNO": stk_code,
        }  
        headers ={
            "content-type": "application/json; charset=utf-8",
            "authorization": f"Bearer {self.ACCESS_TOKEN}",
            "appkey": self.APP_KEY,
            "appsecret": self.APP_SECRET,
            "tr_id": "TTTC8408R",
            "custtype": "P",
        }
        json_response = await self.send_request('매도가능수량', 'GET', url, headers, params=params)
        try:
            return InquirePsblSell_Response(**json_response)
        except ValidationError as e:
            raise HTTPException(status_code=500, detail=f"Error parsing JSON: {e}")

    ##############################################################################################
    # [국내주식] 업종/기타 > 국내휴장일조회
    # 국내휴장일조회 API입니다.
    # 영업일, 거래일, 개장일, 결제일 여부를 조회할 수 있습니다.
    # 주문을 넣을 수 있는지 확인하고자 하실 경우 개장일여부(opnd_yn)을 사용하시면 됩니다.
    ##############################################################################################
    async def chk_workingday(self, ymd:str) -> ChkWorkingDay_Response:
        '''국내휴장일조회 '''
        logger.info(f"국내휴장일조회")

        url = self.BASE_URL + "/uapi/domestic-stock/v1/quotations/chk-holiday"
        params = {
            "BASS_DT": ymd, #"기준일자 기준일자(YYYYMMDD)",
            "CTX_AREA_NK": "",  # 연속조회키 공백으로 입력",
            "CTX_AREA_FK": "",  # 연속조회검색조건 공백으로 입력",
        }    
        headers ={
            "content-type": "application/json; charset=utf-8",
            "authorization": f"Bearer {self.ACCESS_TOKEN}",
            "appkey": self.APP_KEY,
            "appsecret": self.APP_SECRET,
            "tr_id": "CTCA0903R",
            "custtype": "P"
        }    
        json_response = await self.send_request('국내휴장일조회', 'GET', url, headers, params=params)
        try:
            return ChkWorkingDay_Response(**json_response)
        except ValidationError as e:
            raise HTTPException(status_code=500, detail=f"Error parsing JSON: {e}")
        
    # -------------------------------------------------------------------------------
    # 순위분석
    # -------------------------------------------------------------------------------
    async def after_hour_balance(self, req:AfterHourBalance_Request) -> AfterHourBalance_Response:
        '''시간외호가잔량순위 '''
        logger.info(f"시간외호가잔량순위")

        url = self.BASE_URL + "/uapi/domestic-stock/v1/ranking/after-hour-balance"
        params = {
            "fid_input_price_1":  req.fid_input_price_1, #입력 가격1 입력값 없을때 전체 (가격 ~)
            "fid_cond_mrkt_div_code": req.fid_cond_mrkt_div_code, #"조건 시장 분류 코드 시장구분코드 (주식 J)",
            "fid_cond_scr_div_code": req.fid_cond_scr_div_code,  #"조건 화면 분류 코드 Unique key( 20176 )",
            "fid_rank_sort_cls_code": req.fid_rank_sort_cls_code, # "순위 정렬 구분 코드 1: 장전 시간외, 2: 장후 시간외, 3:매도잔량, 4:매수잔량",
            "fid_div_cls_code": req.fid_div_cls_code, # "분류 구분 코드 0 : 전체",
            "fid_input_iscd": req.fid_input_iscd,   #입력 종목코드 0000:전체, 0001:거래소, 1001:코스닥, 2001:코스피200",
            "fid_trgt_exls_cls_code": req.fid_trgt_exls_cls_code, # "대상 제외 구분 코드 0 : 전체",
            "fid_trgt_cls_code": req.fid_trgt_cls_code, # 대상 구분 코드 0 : 전체",
            "fid_vol_cnt": req.fid_vol_cnt, # 거래량 수 입력값 없을때 전체 (거래량 ~)",
            "fid_input_price_2": req.fid_input_price_2 #입력 가격2 입력값 없을때 전체 (~ 가격)",        
        }    
        headers ={
                "content-type": "application/json; charset=utf-8",
                "authorization": f"Bearer {self.ACCESS_TOKEN}",
                "appkey": self.APP_KEY,
                "appsecret": self.APP_SECRET,
                "tr_id": "FHPST01760000",
                "custtype":  "P" 
        }    
        json_response = await self.send_request('시간외호가잔량순위', 'GET', url, headers, params=params)
        try:
            return AfterHourBalance_Response(**json_response)
        except ValidationError as e:
            raise HTTPException(status_code=500, detail=f"Error parsing JSON: {e}")
    
    async def quote_balance(self, req:QuoteBalance_Request) -> QuoteBalance_Response:
        '''호가잔량순위 '''
        logger.info(f"호가잔량순위")

        url = self.BASE_URL + "/uapi/domestic-stock/v1/ranking/quote-balance"
        params = {
            "fid_vol_cnt": req.fid_vol_cnt, # "거래량 수 입력값 없을때 전체 (거래량 ~)",
            "fid_cond_mrkt_div_code":req.fid_cond_mrkt_div_code, # 조건 시장 분류 코드 시장구분코드 (주식 J)",
            "fid_cond_scr_div_code": req.fid_cond_scr_div_code,  #조건 화면 분류 코드 Unique key( 20172 )",
            "fid_input_iscd": req.fid_input_iscd, #입력 종목코드 0000(전체) 코스피(0001), 코스닥(1001), 코스피200(2001)",
            "fid_rank_sort_cls_code": req.fid_rank_sort_cls_code, #순위 정렬 구분 코드 0: 순매수잔량순, 1:순매도잔량순, 2:매수비율순, 3:매도비율순",
            "fid_div_cls_code": req.fid_div_cls_code, #분류 구분 코드 0:전체",
            "fid_trgt_cls_code": req.fid_trgt_cls_code, #대상 구분 코드 0:전체",
            "fid_trgt_exls_cls_code": req.fid_trgt_exls_cls_code, #대상 제외 구분 코드 0:전체",
            "fid_input_price_1": req.fid_input_price_1, #입력 가격1 입력값 없을때 전체 (가격 ~)",
            "fid_input_price_2": req.fid_input_price_2, #입력 가격2 입력값 없을때 전체 (~ 가격)",      
        }    
        headers ={
            "content-type": "application/json; charset=utf-8",
            "authorization": f"Bearer {self.ACCESS_TOKEN}",
            "appkey": self.APP_KEY,
            "appsecret": self.APP_SECRET,
            "tr_id": "FHPST01720000",
            "custtype": "P" # 법인 P : 개인",
        }    
        json_response = await self.send_request('호가잔량순위', 'GET', url, headers, params=params)
        try:
            return QuoteBalance_Response(**json_response)
        except ValidationError as e:
            raise HTTPException(status_code=500, detail=f"Error parsing JSON: {e}")