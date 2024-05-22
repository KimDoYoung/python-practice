from io import StringIO
import os
import random
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import datetime


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

# def split_title_count(span_text):
#     # 정규 표현식 패턴 정의
#     pattern = r'([\w\s]+)(?:\((\d+)\))?'
    
#     # 패턴 매칭 시도
#     match = re.match(pattern, span_text)
    
#     if match:
#         word = match.group(1)  # 첫 번째 그룹: 단어
#         number = match.group(2)  # 두 번째 그룹: 숫자 (있을 경우)
        
#         if number:
#             return word, int(number)
#         else:
#             return word, None
#     else:
#         return span_text, None  # 패턴에 맞지 않는 경우 원본 문자열과 None 반환

# def get_save_path(theme):
#     # Create a directory to save the data
#     today = datetime.datetime.now().strftime("%Y_%m_%d")
#     save_path = f'data/{today}'
#     os.makedirs(save_path, exist_ok=True)
#     theme = theme.replace(" ", "_")
#     filename = f'{save_path}/{theme}.csv'
#     return filename

def create_base_folder(base):
    now_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    save_path = f'{base}/{now_time}'
    os.makedirs(save_path, exist_ok=True)
    return save_path

def df_change(df):
    
    cost_range_pattern = r'([0-9,-]+)\s*([0-9,-]+)'
    percent_range_pattern = r'(-?\d+\.\d+%)\s*(-?\d+\.\d+%)?'
    if '현재가격' in df.columns:
        try:
            df[['전일가', '등락가']] = df['현재가격'].str.extract(cost_range_pattern)
            df['전일가'] = df['전일가'].fillna(0)
            df['등락가'] = df['등락가'].fillna(0)
        except ValueError as e:
            print(f"Error extracting '현재가격': {e}")

        df['전일가'] = df['전일가'].str.replace(',', '').astype(int)
        df['등락가'] = df['등락가'].str.replace(',', '').astype(int)

    if '52주 최고최저' in df.columns:
        try:
            df[['52주최고', '52주최저']] = df['52주 최고최저'].str.extract(cost_range_pattern)
        
            df['52주최고'] = df['52주최고'].fillna(0)
            df['52주최저'] = df['52주최저'].fillna(0)
        except ValueError as e:
            print(f"Error extracting '52주 최고최저': {e}")
        
        df['52주최고'] = df['52주최고'].str.replace(',', '').astype(int)
        df['52주최저'] = df['52주최저'].str.replace(',', '').astype(int)

#52주 변동률
    if '52주 변동률' in df.columns:
        try:
            df[['52주변동률최저', '52주변동률최고']] = df['52주 변동률'].str.extract(percent_range_pattern)
            df['52주변동률최저'] = df['52주변동률최저'].fillna(0)
            df['52주변동률최고'] = df['52주변동률최고'].fillna(0)
        except ValueError as e:
            print(f"Error extracting '52주 변동률': {e}")

        df['52주변동률최저'] = df['52주변동률최저'].astype(str).str.replace('%', '').astype(float)
        df['52주변동률최저'] = df['52주변동률최저'].astype(str).str.replace('%', '').astype(float)

    if '3년 최고최저' in df.columns:
        try:
            df[['3년최고', '3년최저']] = df['3년 최고최저'].str.extract(cost_range_pattern)
            df['3년최고'] = df['3년최고'].fillna(0)
            df['3년최저'] = df['3년최저'].fillna(0)
        except ValueError as e:
            print(f"Error extracting '3년 최고최저': {e}")
        
        df['3년최고'] = df['3년최고'].str.replace(',', '').astype(int)
        df['3년최저'] = df['3년최저'].str.replace(',', '').astype(int)

#3년 최고최저
    percent_range_pattern = r'(-?\d+\.\d+%)\s*(-?\d+\.\d+%)?'
    if '3년 변동률' in df.columns:
        try:
            df[['3년변동률최저', '3년변동률최고']] = df['3년 변동률'].str.extract(percent_range_pattern)
            df['3년변동률최저'] = df['3년변동률최저'].fillna(0)
            df['3년변동률최고'] = df['3년변동률최고'].fillna(0)
        except ValueError as e:
            print(f"Error extracting '3년 변동률': {e}")

        df['3년변동률최저'] = df['3년변동률최저'].astype(str).str.replace('%', '').astype(float)
        df['3년변동률최고'] = df['3년변동률최고'].astype(str).str.replace('%', '').astype(float)

    # df['3년변동률최고'] = df['3년변동률최고'].str.replace(',', '').astype(int)
    if '시가총액' in df.columns:
        df['시가총액억'] = df['시가총액'].apply(to_eak)    

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

def main():
    base_folder = create_base_folder('data')
    # Send a GET request to the website
    url = "https://www.judal.co.kr/"
    response = requests.get(url)

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")
    divs = soup.find_all('div', class_='list-group-item list-group-item-action disabled')
    if len(divs) == 2:
        start_div, end_div = divs


    # # 첫 번째 <div> 태그를 span 텍스트로 찾습니다.
    # start_div = soup.find('div', class_='list-group-item list-group-item-action disabled', string=lambda x: x and '테마 보기' in x)

    # # 두 번째 <div> 태그를 span 텍스트로 찾습니다.
    # end_div = soup.find('div', class_='list-group-item list-group-item-action disabled', string=lambda x: x and '테마별 종목' in x)

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
    # Loop over the 'a' tags
    for tag in a_tags:
        # Extract the href attribute
        href = tag.get('href')
        name, count = split_title_count(tag.find('span').text.strip())
        # name = tag.find('span').text.strip()
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
            print(f"parsing 시작 : {name}, url : {url}")
            table = StringIO(str(table1))
            # Convert table to dataframe
            df = pd.read_html(table)[0]
            # data preprocessing
            # '현재가격' 컬럼을 '전일가'와 '등락가'로 분리
            if '현재가격' in df.columns:
                df = df_change(df)
            elif '테마차트(90일)' in df.columns:
                df = df_change_theme(df)

            filepath = f'{base_folder}/{name.replace("/","_").replace(" ", "_")}.csv'
            df.to_csv(filepath, index=False)
            
            print(filepath + " is saved!")
            scraped_urls.add(url)
            # Generate a random sleep time between 1 and 3 seconds
            sleep_time = random.uniform(1, 5)
            time.sleep(sleep_time)
        else:
            print(f"No table found for {name} at {url}")

    print ("Data scraping is done!")    

if __name__ == "__main__":
    main()
