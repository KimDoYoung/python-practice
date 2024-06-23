# holiday-godata.py
"""
모듈 설명: 
    - 공공데이터(https://www.data.go.kr/)에서 공휴일 정보를 가져와서 
    - MongoDB, EventDays collection에  저장하는 모듈
주요 기능:
    

작성자: 김도영
작성일: 04
버전: 1.0
"""
import asyncio
from datetime import datetime
from beanie import init_beanie
from dateutil.relativedelta import relativedelta
import time
import requests
import xml.etree.ElementTree as ET
from backend.app.core.logger import get_logger
from backend.app.core.mongodb import MongoDb
from backend.app.core.config import config
# from backend.app.core.dependency import get_eventdays_service, get_user_service
from backend.app.core.exception import lucy_exception
from backend.app.domains.system.eventdays_model import EventDays
from backend.app.domains.user.user_model import User

logging = get_logger(__name__)

async def fetch_holidays(year, month):
    from backend.app.core.dependency import  get_user_service
    sYear = str(year)
    sMonth = str(month).zfill(2)

    API_URL = 'http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo'

    user_service = get_user_service()
    #TODO 사용자가 고정되는 것이 맞는가?
    user = await user_service.get_1('kdy987')
    if user:
        API_KEY = user.get_value_by_key('GODATA_DECODE')

    if not API_KEY:
        raise lucy_exception('GODATA_DECODE 키값이 없습니다.')

    params ={'serviceKey' : API_KEY, 'solYear' : sYear, 'solMonth' : sMonth }

    response = requests.get(API_URL, params=params)
    
    if response.status_code == 200:
        logging.debug(response.content)
        return response.content.decode('utf-8')
    else:
        logging.error(f"네트워크오류: Failed to fetch data for {year}-{month}: {response.status_code}")
        return None

def parse_xml_and_update_days(xml_data):
    logging.debug(f"가져온 휴일 데이터 : {xml_data}")
    days = []
    root = ET.fromstring(xml_data)
    
    header = root.find(".//header/resultCode")
    if header is not None and header.text == "00":
        items = root.findall(".//item")
        
        for item in items:
            dateKind = item.find("dateKind").text
            dateName = item.find("dateName").text
            isHoliday = item.find("isHoliday").text
            locdate = item.find("locdate").text
            seq = item.find('seq').text
            days.append({
                'dateKind': dateKind,
                'dateName': dateName,
                'isHoliday': isHoliday,
                'locdate': locdate,
                'seq': seq
            })
    else:
        error_message = root.find(".//cmmMsgHeader/errMsg")
        if error_message is not None:
            logging.error(f"가져온 데이터 오류: {error_message.text}")
        else:
            logging.error("알려지지 않은 오류")
    return days

async def upsert_holidays(days):
    from backend.app.core.dependency import get_eventdays_service
    service = get_eventdays_service()

    for item in days:
        await service.upsert(item)

def future_12_months(year, month):
    ''' year, month를 기준으로 12개월 후까지의 연도와 월을 반환하는 함수 '''
    start_date = datetime(year, month, 1)
    result = []
    for i in range(12):
        future_date = start_date + relativedelta(months=i)
        result.append((future_date.year, future_date.month))
    return result

async def db_init():
    mongodb_url = config.DB_URL
    db_name = config.DB_NAME
    logging.info(f"MongoDB 연결: {mongodb_url} / {db_name}")
    await MongoDb.initialize(mongodb_url)

    db = MongoDb.get_client()[db_name]
    await init_beanie(database=db, document_models=[User])
    await init_beanie(database=db, document_models=[EventDays])

async def fetch_and_upsert_holiday(arg):
    year = datetime.now().year
    month = datetime.now().month
    logging.debug(f"{arg} 현재 연도: {year}, 현재 월: {month}")
    for year, month in future_12_months(year, month):
        xml_data = await fetch_holidays(year, month)
        if xml_data:
            days = parse_xml_and_update_days(xml_data)
            await upsert_holidays(days)
        logging.info(f"{year}년 {month}월 데이터 처리 완료")
        time.sleep(2)


async def main():
    await db_init()
    await fetch_and_upsert_holiday("휴일정보")


#TODO main 함수를 호출하는 코드 추가
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"An error occurred: {e}")
