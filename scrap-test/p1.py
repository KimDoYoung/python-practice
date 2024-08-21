import io
import os
import re
import sys
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import chromedriver_autoinstaller

def install_chrome_driver():
    chromedriver_autoinstaller.install()
# 198.199.86.11	8080	United States	
# 139.59.1.14	8080	India	
# 209.79.65.132	8080	United States	
# 178.254.143.82	6666	Serbia	

    proxy_ip = "209.79.65.132"
    proxy_port = "8080"
    # proxy = f"http://{proxy_ip}:{proxy_port}"

    # Chrome 옵션 설정
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Headless 모드 활성화
    chrome_options.add_argument("--disable-gpu")  # GPU 가속 비활성화
    chrome_options.add_argument('--no-sandbox')  # Bypass OS security model, 크롬의 일반적인 문제 해결 옵션
    chrome_options.add_argument('--disable-dev-shm-usage')  # 컨테이너 환경에서 메모리 문제를 해결
    #chrome_options.add_argument(f'--proxy-server={proxy}')

    global driver 
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def get_hrefs(url):
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "html")))
    soup =  BeautifulSoup(driver.page_source, 'html.parser')
    #soup.prettify()
    spans = soup.find_all('span', class_='list-item item-name item-title')

    # 각 span 안에 있는 anchor 태그 추출 및 출력
    # for span in spans:
    #     anchors = span.find_all('a')
    #     for anchor in anchors:
    #         print(anchor['href'], anchor.text)    
    ol = soup.find('ol', id='torrents')

    data = []
    for li in ol.find_all('li', class_='list-entry'):
        row = [span.text for span in li.find_all('span', class_="list-item")]
        href = li.find('span', class_="item-title").a['href']
        row.append(href)
        data.append(row)

    print(f"{url} : 갯수: ", len(data))

    # # 최대 열 수 찾기
    # max_columns = max(len(row) for row in data)

    # # 각 행의 길이를 최대 열 수에 맞추기 (None으로 패딩)
    # for row in data:
    #     while len(row) < max_columns:
    #         row.append(None)

    # # 데이터프레임으로 변환
    # df = pd.DataFrame(data, columns=[f'Column {i+1}' for i in range(max_columns)])

    df = pd.DataFrame(data, columns=['type','name','uploaded',
                    'size',
                    'seed',
                    'leech',
                    'user', 'href']
                    )
    
    df = df.drop('type', axis=1)
    
    print(df['leech'].dtype)
    print("------------------------------------------------")
    print(df[['leech', 'name']])
    print("------------------------------------------------")
    # 공백 제거
    df['leech'] = df['leech'].str.strip()
    # 특정 패턴의 문자열을 대체
    df['leech'] = df['leech'].apply(lambda x: re.sub(r'[^0-9]', '', x) if isinstance(x, str) else x)
    df['leech'] = pd.to_numeric(df['leech'], errors='coerce')
    # print(df['leech'].dtype)
    # print(df[['leech', 'name']])

    # 'leech' 열을 정수로 변환. 변환할 수 없는 값은 NaN으로 처리
    #print(df[['leech', 'name']])
    # NaN 값을 포함하는 행 제거
    #df = df.dropna(subset=['leech'])    
    df = df[df['leech'] >= 100]
    # print(df[['leech', 'name']])
    # print(df['href'].to_list())
    # href_array = df['href'].to_list()
    return df

def main():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    driver = install_chrome_driver()
    load_dotenv()

    # 환경 변수 사용
    baseUrl = os.getenv('P_URL')

    df_all = pd.DataFrame()
    for i in range(0, 2):
        url = f"{baseUrl}/search.php?q=user:Cristie65:{i}"
        new_df = get_hrefs(url)
        df_all = pd.concat([df_all, new_df], ignore_index=True)

    df_all['href'] = baseUrl +  df_all['href']

    df_all.to_csv('torrent.csv', index=False)
    print("torrent.csv saved")
    print("Done!")    

if __name__ == "__main__":
    main()