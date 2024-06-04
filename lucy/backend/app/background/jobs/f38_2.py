# f38_2.py
"""
모듈 설명: 
collection ipo_scrap_38 에 쌓여 있는 데이터를 1. 가공하고  2. 필요한 데이터만 Ipo 컬렉션으로 옮긴다.

주요 기능:
- 컬렉션 Config의 last-fetch-time을 조회하여 마지막 스크랩 시간을 확인
- last-fetch-time 이후에 스크랩된 데이터를 조회 하여 가공 선별하여 Ipo Collection에 넣는다.
- 넣는 방법은 upsert 방식으로 처리한다.
- last-fetch-time을 업데이트 한다.

작성자: 김도영
작성일: 2024-05-29
버전: 1.0
"""

import asyncio
from pymongo import  MongoClient, UpdateOne
from datetime import datetime
from backend.app.core.mongodb import MongoDb
from backend.app.utils.scrap_util import extract_competition_rates, extract_dates, extract_numbers, to_num, to_won, to_ymd
from backend.app.core.logger import get_logger 
from backend.app.core.config import config

logging = get_logger(__name__)

def get_title(company_info):
    title = f"{company_info['종목명']}-{company_info['진행상황']}-{company_info['시장구분']}({company_info['종목코드']})"
    return title

def get_days(schedule_info): 
    days = {}
    day = schedule_info['공모청약일']
    sdate,edate = extract_dates(day)
    days['청약일'] = edate
    days['납입일'] = to_ymd(schedule_info['납입일'])
    days['환불일'] = to_ymd(schedule_info['환불일'])
    days['상장일'] = to_ymd(schedule_info['상장일'])

    return days

def get_offering(offering_info, expected_participation):
    logging.info('offering_info: %s', offering_info)
    offering = {}
    offering['총공모주식수'] = to_num(offering_info['총공모주식수'])
    offering['액면가'] = to_num(offering_info['액면가'])
    offering['확정공모가'] = to_won(offering_info['확정공모가'])
    company_list = []
    scrap_company_list = offering_info['주간사_리스트']
    for company in scrap_company_list:
        item = {}
        item['주간사'] = company['인수회사']
        start, end = extract_numbers('' if company['청약한도'] is None else company['청약한도'])
        item['청약한도'] = start
        company_list.append(item)

    offering['주간사_리스트'] = company_list
    competition_rate = {}
    
    if '단순경쟁' in expected_participation:
        cr1, cr2 = extract_competition_rates(expected_participation['단순경쟁'])
    else:
        cr1, cr2 = None, None    
    competition_rate['균등'] = cr1
    competition_rate['비례'] = cr2
    offering['경쟁율'] = competition_rate
    return offering

async def work1(db, all_data=False):
    
    ''' 38사이트에서 스크랩한 원본 collection ipo_scrap에서 ipo 컬렉션으로 옮긴다. 1.필요한것만, 2.format변환 '''
    # client = MongoClient('mongodb://root:root@test.kfs.co.kr:27017/')
    logging.info("-------------------------------------") 
    logging.info('scrap38_2_ipo() started')
    logging.info("-------------------------------------") 

    collection_scrap = db['ipo_scrap_38']
    collection_ipo = db['Ipo']
    collection_config = db['Config']

    # last_fetch_config = collection_config.find_one({'key': 'scap_to_ipo_time'})
    # if last_fetch_config:
    #     last_fetch_time = last_fetch_config['value']
    # else:
    #     last_fetch_time = datetime(1970, 1, 1)  # 기본값으로 먼 과거의 시간을 설정

    # if all_data:
    #     last_fetch_time = datetime(1970, 1, 1)  # 기본값으로 먼 과거의 시간을 설정    
    #     logging.info('all data will be processed.')

    last_fetch_time = datetime(1970, 1, 1)
    logging.info(f"Last fetch time: {last_fetch_time}") 

    query = {'scrap_time': {'$gt': last_fetch_time}}
    documents = collection_scrap.find({})
    document_count = await collection_scrap.count_documents({})
    logging.info("-------------------------------------") 
    logging.info(f"scraping 조회 끝 {document_count}개의 문서가 조회되었습니다.")
    logging.info("-------------------------------------") 

    ipo_list = []

    async for doc in documents:
        name = doc['stk_name']
        logging.info(f"-------->Processing document for {name}")
        details = doc['details']
        # 필수 키가 있는지 확인
        required_keys = ['company_info', 'schedule_info', 'offering_info', 'expected_participation']
        if not all(key in details for key in required_keys):
            logging.warning(f"Document {doc['_id']} is missing one of the required keys: {required_keys}")
            continue        

        company_info = details['company_info']
        schedule_info = details['schedule_info']
        offering_info = details['offering_info']
        expected_participation = details['expected_participation']
        new_stk_name = company_info['종목명']  + '-' + company_info['종목코드']  
        processed_entry = {
            'stk_name' : new_stk_name,  #doc['stk_name'],
            'name' : company_info['종목명'],
            'title' : get_title(company_info),
            'days' : get_days(schedule_info),
            'offering' : get_offering(offering_info, expected_participation),
            'processed_time': datetime.now(),
            'scrap_id': doc['_id'],  # 원본 문서의 ObjectId 추가
        }
        ipo_list.append(processed_entry)

    # upsert 작업을 위한 요청 목록 생성
    requests = []
    for entry in ipo_list:
        requests.append(
            UpdateOne(
                {'stk_name': entry['stk_name']},
                {'$set': entry},
                upsert=True
            )
        )

    if requests:
        result = await collection_ipo.bulk_write(requests)
        logging.info(f"Bulk write result: {result.bulk_api_result}")
    else:
        logging.warning("No data to insert into ipo collection.")

    # Step 3: config 컬렉션에 last-fetch-time 업데이트
    current_time = datetime.now()
    current_time_str = current_time.isoformat()
    await collection_config.update_one(
        {'key': '38-scrapping-time'},
        {'$set': {'value': current_time_str}},
        upsert=True
    )
    logging.info("Config collection updated with current fetch time.")

async def main():
    url = config.DB_URL
    dbname = config.DB_NAME
    await MongoDb.initialize(url)
    client = MongoDb.get_client()
    db = client[dbname]
    await work1(db, all_data=True)
    logging.info('-------------------------------------')   
    logging.info('scrap38_2_ipo() finished')
    logging.info('-------------------------------------')   


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        logging.info("Main execution completed.")