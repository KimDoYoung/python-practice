# judal_scrap_1.py
"""
모듈 설명: 
    - '주달' 사이트를 scrapping한다 
    - database를 사용하지 않고 csv파일을 사용한다.
    - 검색기능으로 투자할 종목을 찾을 때 사용하려는 의도로 scrapping함

주요 기능:
    - site "https://www.judal.co.kr/" 을 scrapping
    - scrapping한 파일들은  config DATA_FOLDER 폴더 하위에 judal 밑에 ymd_time 폴더밑에 csv로 쌓인다.
    - 크론으로 동작하게끔한다.

작성자: 김도영
작성일: 29
버전: 1.0
"""
from io import StringIO
import os
import random
import time
from fastapi import Depends
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import datetime
from backend.app.core.config import config
from backend.app.core.logger import get_logger
from backend.app.domains.system.config_service import DbConfigService
from dependency import get_config_service

logging = get_logger(__name__)

def to_eak(value):
    # '조'와 '억원' 단위를 처리하여 숫자로 변환하는 함수
    value = value.replace(' ', '')  # 공백 제거
    if '조' in value and '억원' in value:
        parts = value.split('조')
        trillions = int(parts[0])
        billions = int(parts[1].replace('억원', ''))
        return trillions * 10000 + billions
    elif '조' in value:
        return int(value.replace('조', '')) * 10000
    elif '억원' in value:
        return int(value.replace('억원', ''))
    else:
        return int(value)
    
def split_title_count(span_text):
    # 정규 표현식을 사용하여 패턴 매칭
    match = re.match(r'^(.*)\((\d+)\)$', span_text)
    if match:
        # 첫 번째 그룹은 '원자재(구리)'와 두 번째 그룹은 '6'을 포함
        return match.group(1), int(match.group(2))
    else:
        return None, None


def create_base_folder(base : str):
    now_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    save_path = f'{base}/{now_time}'
    os.makedirs(save_path, exist_ok=True)
    return save_path

def df_change(df):
    
    cost_range_pattern = r'([0-9,-]+)\s*([0-9,-]+)'
    percent_range_pattern = r'(-?\d+\.\d+%)\s*(-?\d+\.\d+%)?'
    if '종목명' in df.columns:
        array1 = df['종목명'].str.split(' ')
        df['종목명'] = array1.str[0]
        df['시장종류'] = array1.str[1]
        df['종목코드'] = array1.str[2]

    if '현재가격' in df.columns:
        try:
            df[['현재가', '등락가']] = df['현재가격'].str.extract(cost_range_pattern)
            df['현재가'] = df['현재가'].fillna(0)
            df['등락가'] = df['등락가'].fillna(0)
        except ValueError as e:
            logging.error(f"Error extracting '현재가격': {e}")

        df['현재가'] = df['현재가'].str.replace(',', '').astype(int)
        df['등락가'] = df['등락가'].str.replace(',', '').astype(int)
        df.drop(columns=['현재가격'], inplace=True)

    if '52주 최고최저' in df.columns:
        try:
            df[['52주최고', '52주최저']] = df['52주 최고최저'].str.extract(cost_range_pattern)
        
            df['52주최고'] = df['52주최고'].fillna(0)
            df['52주최저'] = df['52주최저'].fillna(0)
        except ValueError as e:
            logging.error(f"Error extracting '52주 최고최저': {e}")
        
        df['52주최고'] = df['52주최고'].str.replace(',', '').astype(int)
        df['52주최저'] = df['52주최저'].str.replace(',', '').astype(int)
        df.drop(columns=['52주 최고최저'], inplace=True)

#52주 변동률
    if '52주 변동률' in df.columns:
        try:
            df[['52주변동률최저', '52주변동률최고']] = df['52주 변동률'].str.extract(percent_range_pattern)
            df['52주변동률최저'] = df['52주변동률최저'].fillna(0)
            df['52주변동률최고'] = df['52주변동률최고'].fillna(0)
        except ValueError as e:
            logging.error(f"Error extracting '52주 변동률': {e}")

        df['52주변동률최저'] = df['52주변동률최저'].astype(str).str.replace('%', '').astype(float)
        df['52주변동률최저'] = df['52주변동률최저'].astype(str).str.replace('%', '').astype(float)
        df.drop(columns=['52주 변동률'], inplace=True)

    if '3년 최고최저' in df.columns:
        try:
            df[['3년최고', '3년최저']] = df['3년 최고최저'].str.extract(cost_range_pattern)
            df['3년최고'] = df['3년최고'].fillna(0)
            df['3년최저'] = df['3년최저'].fillna(0)
        except ValueError as e:
            logging.error(f"Error extracting '3년 최고최저': {e}")
        
        df['3년최고'] = df['3년최고'].str.replace(',', '').astype(int)
        df['3년최저'] = df['3년최저'].str.replace(',', '').astype(int)
        df.drop(columns=['3년 최고최저'], inplace=True)

#3년 최고최저
    percent_range_pattern = r'(-?\d+\.\d+%)\s*(-?\d+\.\d+%)?'
    if '3년 변동률' in df.columns:
        try:
            df[['3년변동률최저', '3년변동률최고']] = df['3년 변동률'].str.extract(percent_range_pattern)
            df['3년변동률최저'] = df['3년변동률최저'].fillna(0)
            df['3년변동률최고'] = df['3년변동률최고'].fillna(0)
        except ValueError as e:
            logging.error(f"Error extracting '3년 변동률': {e}")

        df['3년변동률최저'] = df['3년변동률최저'].astype(str).str.replace('%', '').astype(float)
        df['3년변동률최고'] = df['3년변동률최고'].astype(str).str.replace('%', '').astype(float)
        df.drop(columns=['3년 변동률'], inplace=True)

    # df['3년변동률최고'] = df['3년변동률최고'].str.replace(',', '').astype(int)
    if '시가총액' in df.columns:
        df['시가총액'] = df['시가총액'].apply(to_eak)    
    
    if '기대수익률' in df.columns:
        df['기대수익률'] = df['기대수익률'].str.replace('%', '').str.replace(',','').astype(float)

    if '버핏초이스' in df.columns:
        df['버핏초이스'] = df['버핏초이스'].astype(str).str.replace(' ', '').str.replace('위', '')
        df['버핏초이스'] = df['버핏초이스'].replace('nan', '99999').astype(int)        

    return df

def convert_percentage_to_float(value):
    try:
        return float(value.replace('%', ''))
    except ValueError:
        return None

def df_change_theme(df):
    df.drop(columns=['테마차트(90일)'], inplace=True)
    df.drop(columns=['업데이트'], inplace=True)
    df.drop(columns=['테마토크'], inplace=True)
    df['테마명'] = df['테마명'].str.replace('Information', '').str.strip()


    columns_to_convert = ['3년 상승률', '3년 하락률', '52주 상승률', '52주 하락률', '전일비', '3일합산', '기대수익률']
    for column in columns_to_convert:
        df[column] = df[column].apply(convert_percentage_to_float)

    return df

def scrap_judal(config_service : DbConfigService=Depends(get_config_service)):
    
    config_service.set_process_status({"key":"scrap_judal", "value":"running", 'note':'백그라운드 프로세스 scrap_judal is running'})

    data_folder = config.DATA_FOLDER+"/judal"
    base_folder = create_base_folder(data_folder)
    # Send a GET request to the website
    url = "https://www.judal.co.kr/"
    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")
    divs = soup.find_all('div', class_='list-group-item list-group-item-action disabled')
    if len(divs) == 2:
        start_div, end_div = divs

    # theme 별 href 수집
    theme_tag_list = []
    if start_div and end_div:
        for sibling in start_div.find_next_siblings():
            if sibling == end_div:
                break
            if sibling.name == 'a' and 'list-group-item list-group-item-action list-group-item-sub px-4 py-0' in ' '.join(sibling.get('class', '')):
                theme_tag_list.append(sibling)

    theme_list = []
    for a_tag in theme_tag_list:
        theme_list.append({
            'name': a_tag.text.strip(),
            'href': a_tag.get('href')
        })
    df = pd.DataFrame(theme_list)
    df.to_csv(f'{base_folder}/theme_list.csv', index=False)

    #------------------- 개별 theme 별로 데이터 수집 -------------------
    href_list = []
    a_tags = []
    
    if end_div:
        for sibling in end_div.find_next_siblings():
            if sibling.name == 'a':
                a_tags.append(sibling)
            else:
                break            

    for tag in a_tags:
        href = tag.get('href')
        name, count = split_title_count(tag.find('span').text.strip())
        href_list.append({"name": name,  "href": href})

    df = pd.DataFrame(href_list)
    df.to_csv(f'{base_folder}/href_list.csv', index=False)

    scraped_urls = set()

    all_href_list = theme_list + href_list
    

    for item in all_href_list:
        url = item['href']
        name = item['name']
        if url in scraped_urls:
            continue

        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        table1 = soup.find('table', class_='table table-sm table-bordered table-hover align-middle small')
        
        if table1:
            logging.debug(f"parsing 시작 : {name}, url : {url}")
            table = StringIO(str(table1))
            df = pd.read_html(table)[0]
            # 현재가격이 있는 것은 종목, 테마차트(90일)이 있는 것은 테마
            if '현재가격' in df.columns:
                df = df_change(df)
            elif '테마차트(90일)' in df.columns:
                df = df_change_theme(df)

            filepath = f'{base_folder}/{name.replace("/","_").replace(" ", "_")}.csv'
            df.to_csv(filepath, index=False)
            
            logging.debug(filepath + " 저장됨")
            scraped_urls.add(url)

            # random 1초~5초 사이의 sleep
            sleep_time = random.uniform(1, 5)
            time.sleep(sleep_time)
        else:
            logging.error(f"No table found for {name} at {url}")

    logging.debug("Data scraping is done!")    
    config_service.remove_process_status("scrap_judal")

# if __name__ == "__main__":
#     main()
