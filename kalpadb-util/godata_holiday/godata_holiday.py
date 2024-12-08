# godata_holiday.py
"""
모듈 설명: 
    - GODATA 휴일 정보 xml 파일을 가져와서 파싱한 후 kalpadb의 calendar에 넣는다.

작성자: 김도영
작성일: 2024-12-08
버전: 1.0
"""

from datetime import datetime
import time
import os
import sys
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
import pymysql
import requests
import xml.etree.ElementTree as ET

# .env 파일 로드
load_dotenv()

# DB 설정
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT', 3306)),  # 기본 포트 3306
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'charset': os.getenv('DB_CHARSET', 'utf8mb4')  # 기본 문자셋 utf8mb4
}


def parse_xml_and_update_days(xml_data):
    # print(f"가져온 휴일 데이터 : {xml_data}")
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
    """
    MariaDB의 calendar 테이블에 데이터를 중복 여부 확인 후 INSERT하는 함수.
    :param days: list 형태의 공휴일 데이터들
    """
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            # SELECT로 중복 여부 확인
            select_sql = """
            SELECT COUNT(*) FROM calendar
            WHERE gubun = %s AND sorl = %s AND ymd = %s AND content = %s
            """
            
            # INSERT SQL
            insert_sql = """
            INSERT INTO calendar (gubun, sorl, ymd, content, modify_dt)
            VALUES (%s, %s, %s, %s, %s)
            """
            
            for day in days:
                # 데이터 추출
                gubun = 'H'
                sorl = 'S'
                ymd = day['locdate']
                content = day['dateName']
                modify_dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 현재 시간

                # 중복 체크
                cursor.execute(select_sql, (gubun, sorl, ymd, content))
                count = cursor.fetchone()[0]

                if count == 0:
                    # 중복되지 않으면 INSERT
                    cursor.execute(insert_sql, (gubun, sorl, ymd, content, modify_dt))
                    print(f"Inserted: {day}")
                else:
                    print(f"Skipped (duplicate): {day}")
            
            # 한 번에 커밋
            connection.commit()
            print(f"처리 완료: {len(days)}개의 데이터 중 INSERT가 필요한 경우만 처리되었습니다.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        connection.close()


def fetch_holidays(year, month):
    ''' GODATA API를 이용해 특정 연도와 월의 휴일 정보를 가져오는 함수 '''
    sYear = str(year)
    sMonth = str(month).zfill(2)

    API_URL = 'http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo'

    #API_KEY 를 환경변수에서 dotenv로 가져온다
    API_KEY = os.getenv('GODATA_API_KEY')

    params ={'serviceKey' : API_KEY, 'solYear' : sYear, 'solMonth' : sMonth }

    response = requests.get(API_URL, params=params)
    
    if response.status_code == 200:
        data = response.content.decode('utf-8')
        print("--------------- 가져온 데이터 ---------------")
        print(data)
        print("------------------------------------------")
        return data
    else:
        print(f"네트워크오류: Failed to fetch data for {year}-{month}: {response.status_code}")
        return None
    
def future_12_months(year, month):
    ''' year, month를 기준으로 12개월 후까지의 연도와 월을 반환하는 함수 '''
    start_date = datetime(year, month, 1)
    result = []
    for i in range(12):
        future_date = start_date + relativedelta(months=i)
        result.append((future_date.year, future_date.month))
    return result

def fetch_and_upsert_holiday(year: int, month: int):
    ''' 특정 연도와 월의 휴일 정보를 가져와서 DB에 저장하는 함수 '''
    for year, month in future_12_months(year, month):
        xml_data = fetch_holidays(year, month)
        if xml_data:
            days = parse_xml_and_update_days(xml_data)
            upsert_holidays(days)
        print(f"{year}년 {month}월 데이터 처리 완료")
        time.sleep(2)

def main():
    # 인자 개수 확인
    year = datetime.now().year
    month = datetime.now().month

    if len(sys.argv) == 2:
        year = int(sys.argv[1])
    elif len(sys.argv) == 3:
        year = int(sys.argv[1])
        month = int(sys.argv[2])

    fetch_and_upsert_holiday(year, month)

if __name__ == '__main__':
    main()
    print("완료")