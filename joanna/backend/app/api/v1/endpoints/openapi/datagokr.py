from dataclasses import asdict
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import requests
import xml.etree.ElementTree as ET
from backend.app.core.logger import get_logger
from backend.app.core.template_engine import render_template
from backend.app.domains.openapi.godata_model import StockPriceRequest
from backend.app.core.configs import DATA_GO_KR_API_KEY

from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
import urllib.parse

logger = get_logger(__name__)

router = APIRouter()

template_base = "openapi/datagokr"

class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context()
        # 필요한 SSL 버전을 명시적으로 지정, 예: TLSv1_2
        context.set_ciphers('DEFAULT@SECLEVEL=1')
        kwargs['ssl_context'] = context
        return super(SSLAdapter, self).init_poolmanager(*args, **kwargs)

# API 연결에 사용할 어댑터를 설정
adapter = SSLAdapter()

session = requests.Session()
session.mount('https://', adapter)

@router.get("/datagokr/stock/prices", response_class=HTMLResponse)
async def datagokr_stock_prices():
    '''
    금융위원회 주식시세정보
    '''
    logger.debug("금융위원회 주식시세정보 폼 display")
    context = {}
    return render_template(f"{template_base}/stock_price_info.html", context)    


@router.post("/datagokr/stock/prices")
async def datagokr_stock_prices1(stock_price_request: StockPriceRequest):
    '''
    금융위원회 주식시세정보
    '''
    logger.debug("금융위원회 주식시세정보 폼 POST")
    api_key = DATA_GO_KR_API_KEY
    #api_key = "1ROBN6Q1t6iYO9fc2SbHVby0AruUb78/jd0Ruzvyv33tgJKV7WcOyZ+SmhnNPIYmrR0/ppqifPYDcrywywu9ZQ=="
    api_key = urllib.parse.unquote(api_key)
    url= "https://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo"
    params = asdict(stock_price_request)
    params["serviceKey"] = api_key
    # None 값 제거 (dict comprehension을 사용)
    params = {k: v for k, v in params.items() if v is not None}
    logger.debug(f"params: {params}")
    response = session.get(url, params=params)
    logger.debug(f"response: {response}")
    # 응답 처리
    erro_response_json = {}
    response_json = {}
    if response.status_code == 200:
        logger.debug("요청 성공:")
        if is_data_go_error(response.text):
            erro_response_json = get_error_response(response.text)
        else:
            response_json =get_parsing_response(response.text)
            logger.debug(f"godata로 받은 json: {response_json}" )
    else:
        logger.debug("요청 실패, 상태 코드: ", response.status_code)
    context = {"error" : erro_response_json, "list" : response_json}
    return context
    #return render_template(f"{template_base}/stock_price_info.html", context)


def is_data_go_error(response_text):
    # 이 함수는 응답이 에러인지 확인합니다. 실제 구현은 응답 구조에 따라 다를 수 있습니다.
    return "<cmmMsgHeader>" in response_text

import json

def get_parsing_response(xml_data):
    '''정상적 데이터가 XML로 왔었을 때 파싱하는 함수'''
    try:
        root = ET.fromstring(xml_data)
        items = root.findall('.//item')  # 모든 'item' 요소 찾기
        results = []
        for item in items:
            # 각 'item' 요소에서 필요한 데이터를 추출하여 딕셔너리로 생성
            item_dict = {
                "basDt": item.find('basDt').text,
                "srtnCd": item.find('srtnCd').text,
                "isinCd": item.find('isinCd').text,
                "itmsNm": item.find('itmsNm').text,
                "mrktCtg": item.find('mrktCtg').text,
                "clpr": item.find('clpr').text,
                "vs": item.find('vs').text,
                "fltRt": item.find('fltRt').text,
                "mkp": item.find('mkp').text,
                "hipr": item.find('hipr').text,
                "lopr": item.find('lopr').text,
                "trqu": item.find('trqu').text,
                "trPrc": item.find('trPrc').text,
                "lstgStCnt": item.find('lstgStCnt').text,
                "mrktTotAmt": item.find('mrktTotAmt').text
            }
            results.append(item_dict)
        return results  # 주식 데이터의 리스트를 반환
    except ET.ParseError:
        return {"Error": "Failed to parse XML data"}
    except AttributeError:
        return {"Error": "Missing some elements in XML structure"}

def get_error_response(xml_data):
    ''' data.go.kr에서 오는 오류응답 '''
    try:
        root = ET.fromstring(xml_data)
        error_message = root.find('.//errMsg').text
        auth_message = root.find('.//returnAuthMsg').text
        reason_code = root.find('.//returnReasonCode').text
        return {
            "Error Message": error_message,
            "Authorization Message": auth_message,
            "Reason Code": reason_code
        }
    except ET.ParseError:
        return {"Error": "Failed to parse XML data"}