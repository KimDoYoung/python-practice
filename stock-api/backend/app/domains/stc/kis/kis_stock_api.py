# kis_api.py
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
from datetime import datetime
import json
from fastapi import HTTPException
from pydantic import ValidationError
import requests

from backend.app.core.logger import get_logger
from backend.app.domains.stc.kis.model.kis_chk_holiday_model import ChkHolidayDto
from backend.app.domains.stc.kis.model.kis_inquire_balance_model import KisInquireBalance_Response
from backend.app.domains.stc.kis.model.kis_inquire_daily_ccld_model import InquireDailyCcldDto, InquireDailyCcldRequest
from backend.app.domains.stc.kis.model.kis_inquire_price import InquirePrice_Response
from backend.app.domains.stc.kis.model.kis_inquire_psbl_rvsecncl_model import InquirePsblRvsecnclDto
from backend.app.domains.stc.kis.model.kis_inquire_psbl_sell_model import InquirePsblSellDto
from backend.app.domains.stc.kis.model.kis_inquire_psble_order import InquirePsblOrderDto, InquirePsblOrderRequest
from backend.app.domains.stc.kis.model.kis_order_cash_model import KisOrderCancelRequest, OrderCash_Request, KisOrderCash_Response, KisOrderCancelResponse
from backend.app.domains.stc.kis.model.kis_psearch_result_model import PsearchResultDto
from backend.app.domains.stc.kis.model.kis_search_stock_info_model import SearchStockInfo_Response
from backend.app.domains.stc.kis.model.kis_psearch_title_model import PsearchTitleDto
from backend.app.domains.stc.stock_api import StockApi
from backend.app.domains.user.user_model import StkAccount, User
from backend.app.core.exception.stock_api_exceptions import AccessTokenExpireException, AccessTokenInvalidException, InvalidResponseException, KisApiException
logger = get_logger(__name__)

class KisStockApi(StockApi):

    _BASE_URL = 'https://openapi.koreainvestment.com:9443'
    
    def __init__(self, user:User, account: StkAccount):
        super().__init__(user.user_id, account.account_no)
        self.user = user
        self.account = account
        
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

    def get_access_token_time(self)->datetime:
        if self.ACCESS_TOKEN_TIME:
            return datetime.strptime(self.ACCESS_TOKEN_TIME, "%Y-%m-%d %H:%M:%S")
        else:
            return None
        
    #TODO 시간을 체크해서 23시간 이상이면 다시 발급해야 한다.
    async def initialize(self) -> bool:
        ''' Access Token 존재여부 및  만료 여부 확인 '''

        # 존재여부 체크
        if self.ACCESS_TOKEN is None:
            await self.set_access_token_from_kis()

        # 만료여부 체크
        try:
            cost = self.get_current_price("005930") # 삼성전자
        except AccessTokenExpireException as e:
            await self.set_access_token_from_kis()

        return True    

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

        self.account.set_value('KIS_ACCESS_TOKEN', ACCESS_TOKEN)
        await self.user_service.update_user(self.user.user_id, self.user)
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
            raise AccessTokenExpireException("KIS Access Token Expired(접속토큰이 만료됨)")
        if json['rt_cd'] == '1' and json['msg_cd'] == 'EGW00121':
            raise AccessTokenInvalidException("KIS Access Token Invalid(접속토큰이 유효하지 않음)")

        return None
    def current_cost(self, stk_code:str) -> InquirePrice_Response:
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
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            response_data = response.json()
            logger.debug(f"-------------------------------------------------------------")
            logger.debug(f"API 응답 current_cost : [{response_data}]")
            logger.debug(f"-------------------------------------------------------------")
            return InquirePrice_Response(**response_data)
        except requests.exceptions.HTTPError as e:
            logger.error(f"API 응답 에러 : {e}")
            raise KisApiException(status_code=500, detail=f"API 응답 에러 : {e}")    
        except json.JSONDecodeError as e:
            logger.error("응답이 JSON 형식이 아닙니다.")
            raise InvalidResponseException("응답이 JSON 형식이 아닙니다.")


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
        

    def order(self, order_cash : OrderCash_Request ) -> KisOrderCash_Response:
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
                "ORD_DVSN" : "00", 
                "ORD_QTY" : str(order_cash.qty), 
                "ORD_UNPR" : str(order_cash.cost)
            }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        logger.debug(f"response : {response.text}")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f"Error fetching balance: {response.text}")
        try:
            json_data = response.json()
            kis_order_cash = KisOrderCash_Response(**json_data)
            logger.info(f"주문결과 : {kis_order_cash}")
        except requests.exceptions.JSONDecodeError:
            logger.error(f"Error decoding JSON: {response.text}")
            raise HTTPException(status_code=500, detail="Invalid JSON response")
        except ValidationError as e:
            raise HTTPException(status_code=500, detail=f"Error parsing JSON: {e}")
        return kis_order_cash
    
    def search_stock_info(self, stk_code:str) -> SearchStockInfo_Response:
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
            stock_info = SearchStockInfo_Response(**json_data)
            logger.info(f"상품정보 : {stock_info}")
        except requests.exceptions.JSONDecodeError:
            logger.error(f"Error decoding JSON: {response.text}")
            raise HTTPException(status_code=500, detail="Invalid JSON response")
        except ValidationError as e:
            raise HTTPException(status_code=500, detail=f"Error parsing JSON: {e}")
        return stock_info

    def inquire_balance(self) ->KisInquireBalance_Response:
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
            kis_inquire_balance = KisInquireBalance_Response(**json_data)
        except requests.exceptions.JSONDecodeError:
            logger.error(f"Error decoding JSON: {response.text}")
            raise HTTPException(status_code=500, detail="Invalid JSON response")            
        except ValidationError as e:
            raise HTTPException(status_code=500, detail=f"Error parsing JSON: {e}")

        return kis_inquire_balance

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
    
    def order_cancel(self, order_cancel: KisOrderCancelRequest) -> KisOrderCancelResponse:
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

        response = requests.post(url, headers=headers, data=json.dumps(body))
        logger.debug(f"response : {response.text}")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f"Error 주식일별주문체결조회 : {response.text}")
        try:
            json_data = response.json()
            order_cancel = KisOrderCancelResponse(**json_data)
            logger.debug(f"주식 주문 잔량 전부 취소 됨")
        except requests.exceptions.JSONDecodeError:
            logger.error(f"Error decoding JSON: {response.text}")
            raise HTTPException(status_code=500, detail="Invalid JSON response")
        except ValidationError as e:
            raise HTTPException(status_code=500, detail=f"Error parsing JSON: {e}")
        return order_cancel
    
##############################################################################################
# [국내주식] 주문/계좌 > 주식정정취소가능주문조회[v1_국내주식-004]
##############################################################################################
#주식주문(정정취소) 호출 전에 반드시 주식정정취소가능주문조회 호출을 통해 
#정정취소가능수량(output > psbl_qty)을 확인하신 후 정정취소주문 내시기 바랍니다.
#TODO 테스트 필요
def inquire_psbl_rvsecncl(self) -> InquirePsblRvsecnclDto:
    '''정정취소 가능수량 조회 '''
    logger.info(f"정정취소 가능수량 조회")
    url = self._BASE_URL + "/uapi/domestic-stock/v1/trading/inquire-psbl-rvsecncl"
    params = {
        "CANO": self.ACCTNO[0:8],
        "ACNT_PRDT_CD": self.ACCTNO[8:10],
        "CTX_AREA_FK100": "",  #공란 : 최초 조회시 이전 조회 Output CTX_AREA_FK100 값 : 다음페이지 조회시(2번째부터)",
        "CTX_AREA_NK100": "",  #공란 : 최초 조회시 이전 조회 Output CTX_AREA_NK100 값 : 다음페이지 조회시(2번째부터)",
        "INQR_DVSN_1": "1",  #0 : 조회순서 1 : 주문순 2 : 종목순",
        "INQR_DVSN_2": "1"  #0 : 전체 1 : 매도 2 : 매수",
    }    
    headers ={
        "authorization": f"Bearer {self.ACCESS_TOKEN}",
        "appkey": self.APP_KEY,
        "appsecret": self.APP_SECRET,
        "tr_id":  "TTTC8036R" #모의투자 사용 불가", 
    }       
    response = requests.get(url, headers=headers, params=params)
    logger.debug(f"response : {response.text}")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=f"Error fetching balance: {response.text}")
    try:
        json_data = response.json()
        possible_cancel_result = InquirePsblRvsecnclDto(**json_data)
        logger.info(f"정정취소 가능수량 조회 : {possible_cancel_result}")
    except requests.exceptions.JSONDecodeError:
        logger.error(f"Error decoding JSON: {response.text}")
        raise HTTPException(status_code=500, detail="Invalid JSON response")
    except ValidationError as e:
        raise HTTPException(status_code=500, detail=f"Error parsing JSON: {e}")
    return possible_cancel_result    

##############################################################################################
# [국내주식] 주문/계좌 > 매수가능조회
#############################################################################################
#TODO Test필요
def inquire_psbl_order(self, ipo_req :InquirePsblOrderRequest ) -> InquirePsblOrderDto:
    '''매수가능조회 '''
    logger.info(f"매수가능조회")
    url = self._BASE_URL + "/uapi/domestic-stock/v1/trading/inquire-psbl-order"
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
    response = requests.get(url, headers=headers, params=params)
    logger.debug(f"response : {response.text}")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=f"Error fetching balance: {response.text}")
    try:
        json_data = response.json()
        psbl_order = InquirePsblOrderDto(**json_data)
        logger.info(f"매수가능조회 목록 조회 : {psbl_order}")
    except requests.exceptions.JSONDecodeError:
        logger.error(f"Error decoding JSON: {response.text}")
        raise HTTPException(status_code=500, detail="Invalid JSON response")
    except ValidationError as e:
        raise HTTPException(status_code=500, detail=f"Error parsing JSON: {e}")
    return psbl_order

##############################################################################################
# [국내주식] 업종/기타 > 국내휴장일조회
# 국내휴장일조회 API입니다.
# 영업일, 거래일, 개장일, 결제일 여부를 조회할 수 있습니다.
# 주문을 넣을 수 있는지 확인하고자 하실 경우 개장일여부(opnd_yn)을 사용하시면 됩니다.
##############################################################################################
#TODO Test필요
def chk_holiday(self, base_dt:str) -> ChkHolidayDto:
    '''국내휴장일조회 '''
    logger.info(f"국내휴장일조회")

    url = self._BASE_URL + "/uapi/domestic-stock/v1/quotations/chk-holiday"
    params = {
        "BASS_DT": base_dt, #"기준일자 기준일자(YYYYMMDD)",
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

    response = requests.get(url, headers=headers, params=params)
    logger.debug(f"response : {response.text}")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=f"Error fetching balance: {response.text}")
    try:
        json_data = response.json()
        chk_holiday = InquirePsblOrderDto(**json_data)
        logger.info(f"국내휴장일조회 목록 조회 : {chk_holiday}")
    except requests.exceptions.JSONDecodeError:
        logger.error(f"Error decoding JSON: {response.text}")
        raise HTTPException(status_code=500, detail="Invalid JSON response")
    except ValidationError as e:
        raise HTTPException(status_code=500, detail=f"Error parsing JSON: {e}")
    return chk_holiday

##############################################################################################
# [국내주식] 주문계좌 > 매도가능수량
# [0971] 주식 매도 화면에서 종목코드 입력 후 "가능" 클릭 시 매도가능수량이 확인되는 기능을 API로 개발한 사항
# output > ord_psbl_qty(주문가능수량) 확인하실 수 있습니다.
##############################################################################################
def inquire_psbl_sell(self, stk_code:str) -> InquirePsblSellDto:
    '''매도가능수량 조회 '''
    logger.info(f"매도가능수량 조회")

    url = self._BASE_URL + "/uapi/domestic-stock/v1/trading/inquire-psbl-sell"

    params = {
        "CANO": self.ACCTNO[0:8],
        "ACNT_PRDT_CD": self.ACCTNO[8:10],
        "PDNO": stk_code
    }  
    headers ={
        "content-type": "application/json; charset=utf-8",
        "authorization": f"Bearer {self.ACCESS_TOKEN}",
        "appkey": self.APP_KEY,
        "appsecret": self.APP_SECRET,
        "tr_id": "TTTC8408R",
        "custtype": "p",
    }
    response = requests.get(url, headers=headers, params=params)
    logger.debug(f"response : {response.text}")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=f"Error fetching balance: {response.text}")
    try:
        json_data = response.json()
        inquire_psbl_sell = InquirePsblSellDto(**json_data)
        logger.info(f"매도가능수량조회 : {inquire_psbl_sell}")
    except requests.exceptions.JSONDecodeError:
        logger.error(f"Error decoding JSON: {response.text}")
        raise HTTPException(status_code=500, detail="Invalid JSON response")
    except ValidationError as e:
        raise HTTPException(status_code=500, detail=f"Error parsing JSON: {e}")
    return chk_holiday
