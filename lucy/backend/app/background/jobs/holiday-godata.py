# holiday-godata.py
"""
모듈 설명: 
    - 공공데이터(https://www.data.go.kr/)에서 공휴일 정보를 가져와서 MongoDB에 저장하는 모듈
주요 기능:
    

작성자: 김도영
작성일: 04
버전: 1.0
"""
from datetime import datetime
import logging
import os
import time
import requests
import pymongo
import xml.etree.ElementTree as ET

# TODO DbConfigService에서 API_KEY를 가져오도록 수정
def fetch_holidays(year, month):
    sYear = str(year)
    sMonth = str(month).zfill(2)

    API_URL = 'http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo'
    API_KEY = os.environ.get('GODATA_KEY')

    params ={'serviceKey' : API_KEY, 'solYear' : sYear, 'solMonth' : sMonth }

    response = requests.get(API_URL, params=params)
    
    if response.status_code == 200:
        print(response.content)
        return response.content.decode('utf-8')
    else:
        print(f"네트워크오류: Failed to fetch data for {year}-{month}: {response.status_code}")
        return None

def parse_xml_and_update_days(xml_data):
    print(xml_data)
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
            print(f"가져온 데이터 오류: {error_message.text}")
        else:
            print("알려지지 않은 오류")
    return days

def upsert_holidays(days):
    client = pymongo.MongoClient('mongodb://root:root@test.kfs.co.kr:27017/')
    db = client['stockdb']
    collection = db['holidays']

    for item in days:
        filter = {'locdate': item.get('locdate')}
        update = {'$set': item}
        collection.update_one(filter, update, upsert=True)

def main():
    date_time = datetime.now().strftime("%Y%m%d")

    logging.basicConfig(
        filename=f'holiday_{date_time}.log',  # 로그 파일 경로
        level=logging.INFO,  # 로그 레벨 설정
        format='%(asctime)s - %(levelname)s - %(message)s',  # 로그 메시지 형식
    )    
    year = datetime.now().year
    for month in range(1, 13):
        xml_data = fetch_holidays(year, month)
        if xml_data:
            days = parse_xml_and_update_days(xml_data)
            upsert_holidays(days)
        print(f"{year}년 {month}월 데이터 처리 완료")
        time.sleep(2)

if __name__ == "__main__":
    main()
