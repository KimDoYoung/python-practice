import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient, UpdateOne
from datetime import datetime
from util import extract_competition_rates, extract_dates, extract_numbers, to_num, to_won
from util import to_ymd
import logging  # Import the logging module

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

def scrap_2_ipo(all=False):
    
    ''' 38사이트에서 스크랩한 원본 collection ipo_scrap에서 ipo 컬렉션으로 옮긴다. 1.필요한것만, 2.format변환 '''

    client = MongoClient('mongodb://root:root@test.kfs.co.kr:27017/')
    db = client['stockdb']
    collection_scrap = db['ipo_scrap_38']
    collection_ipo = db['ipo']
    collection_config = db['config']
    
    last_fetch_config = collection_config.find_one({'key': 'last-fetch-time'})
    if last_fetch_config:
        last_fetch_time = last_fetch_config['value']
    else:
        last_fetch_time = datetime(1970, 1, 1)  # 기본값으로 먼 과거의 시간을 설정

    if all:
        last_fetch_time = datetime(1970, 1, 1)  # 기본값으로 먼 과거의 시간을 설정    

    query = {'scrap_time': {'$gt': last_fetch_time}}
    documents = collection_scrap.find(query)

    ipo_list = []

    for doc in documents:
        name = doc['stk_name']
        logging.info(f"-------->Processing document for {name}")
        details = doc['details']
        company_info = details['company_info']
        schedule_info = details['schedule_info']
        offering_info = details['offering_info']
        expected_participation = details['expected_participation']
        processed_entry = {
            'stk_name' : doc['stk_name'],
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
        result = collection_ipo.bulk_write(requests)
        logging.info(f"Bulk write result: {result.bulk_api_result}")
    else:
        logging.warning("No data to insert into ipo collection.")

    # Step 3: config 컬렉션에 last-fetch-time 업데이트
    current_time = datetime.now()
    collection_config.update_one(
        {'key': 'last-fetch-time'},
        {'$set': {'value': current_time}},
        upsert=True
    )
    logging.info("Config collection updated with current fetch time.")

if __name__ == "__main__":

    # 현재 날짜와 시간을 로그 파일 이름에 포함
    date_time = datetime.now().strftime('%Y%m%d')

    # 로그 설정
    logging.basicConfig(
        level=logging.INFO,  # 로그 레벨 설정
        format='%(asctime)s - %(levelname)s - %(message)s',  # 로그 메시지 형식
        handlers=[
            logging.FileHandler(f'scraping_{date_time}.log', encoding='utf-8'),  # 로그 파일 경로
            logging.StreamHandler()  # 콘솔 출력
        ]
    )

    logging.info('------------------------------------------------------')
    logging.info('fetch_38.py started')
    logging.info('------------------------------------------------------')
    scrap_2_ipo(all=True)    
    logging.info('------------------------------------------------------')
    logging.info('fetch_38 ended')
    logging.info('------------------------------------------------------')
