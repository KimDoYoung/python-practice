# kisdoc.py
"""
모듈 설명: 
    kis api document 를 scrapping해서 python code를 만든다.
    https://apiportal.koreainvestment.com/apiservice/oauth2#L_5c87ba63-740a-4166-93ac-803510bb9c02-  
주요 기능:
    - kis api를 selenium을 이용하여 scrapping
    - path에 따른 request/response를 해석해서 python code를 만든다.

작성자: 김도영
작성일: 06
버전: 1.0
"""
from io import StringIO
import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from selenium.common.exceptions import TimeoutException
import pandas as pd

def install_chrome_driver():
    chromedriver_autoinstaller.install()

    # Chrome 옵션 설정
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Headless 모드 활성화
    chrome_options.add_argument("--disable-gpu")  # GPU 가속 비활성화
    chrome_options.add_argument('--no-sandbox')  # Bypass OS security model, 크롬의 일반적인 문제 해결 옵션
    chrome_options.add_argument('--disable-dev-shm-usage')  # 컨테이너 환경에서 메모리 문제를 해결

    global driver 
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def find_and_click_js(driver, xpath):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        driver.execute_script("arguments[0].click();", element)
        return True
    except Exception as e:
        print(f"Error finding or clicking element with xpath '{xpath}': {e}")
        return False

def get_url_and_tables(url:str, menu:str, sub_menu:str):
    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
        # 메인 메뉴 클릭        
        xpath = f"//ul[@class='third-depth']//a[contains(text(), '{menu}')]"
        if not find_and_click_js(driver, xpath):
            print(f"{menu} 로 찾지 못함")
            return

        time.sleep(3)

        # ID가 '업종기간별추이'인 div 요소 찾기
        div_element = driver.find_element(By.ID, sub_menu)
            
        # 해당 div 하위의 클래스가 'btn btn-plus'인 버튼 요소 찾기
        button_element = div_element.find_element(By.CLASS_NAME, "btn-plus")
        button_element.click()
        print("버튼을 클릭했습니다.")

        time.sleep(3)
        # 페이지 소스를 가져와서 BeautifulSoup으로 파싱
        # page_source = driver.page_source
        # with open('page_source.html', 'w', encoding='utf-8') as file:
        #     file.write(page_source)

        dataframes = {}
        soup = BeautifulSoup(page_source, 'html.parser')
        #기본정보 테이블들
        service_list_div = soup.find(id="service-list")
        title_div = service_list_div.find('div', class_='title-depth03')
        if title_div and title_div.find('h4', text='기본정보'):
            # 해당 div 다음에 있는 형제 요소 중 div를 찾기
            next_div = title_div.find_next_sibling('div')
            if next_div:
                dataframes['기본정보'] = pd.read_html(str(next_div))[0]
            else:
                print("기본정보찾기 faile : 다음에 있는 div를 찾을 수 없습니다.")
        else:
            print("기본정보찾기 faile")        


        # ID가 각각 reqHeader, reqBody, resHeader, resBody인 div 요소 내의 테이블을 데이터프레임으로 변환
        ids = ["reqHeader", "reqBody", "resHeader", "resBody"]
        

        for div_id in ids:
            div_element = soup.find(id=div_id)
            if div_element:
                table = div_element.find("table")
                if table:
                    df = pd.read_html(str(table))[0]
                    dataframes[div_id] = df
                    print(f"{div_id} OK")
                    # print(f"{div_id} 데이터프레임:")
                    # print(df)
                else:
                    print(f"{div_id} 안에 테이블이 없습니다.")
            else:
                print(f"{div_id}를 찾을 수 없습니다.")
    except TimeoutException :
        print("페이지 parsing 시간 초과")
        driver.quit()

    return dataframes

def json_pretty(json_str):
    try:
        data_dict = json.loads(json_str)
        s = json.dumps(data_dict, indent=4)
        return s
    except json.JSONDecodeError as e:
        return json_str


def main(menu:str, sub_menu:str):
    driver = install_chrome_driver()
    url = "https://openapi.ls-sec.co.kr/apiservice?group_id=ffd2def7-a118-40f7-a0ab-cd4c6a538a90&api_id=33bd887a-6652-4209-88cd-5324bc7c5e36"
    dataframes = get_url_and_tables(url, menu,sub_menu= sub_menu)    
  
    #드라이버 종료
    driver.quit()

    # 데이터프레임 출력
    for key, df in dataframes.items():
        print(f"{key} 데이터프레임:")
        print(df)
    

if __name__ == "__main__":

    menu = "[업종] 시세"
    sub_menu = "업종기간별추이"
    main(menu, sub_menu)

    print("Done!")