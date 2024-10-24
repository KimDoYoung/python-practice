import re
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def clean_value(value):
    # 정규 표현식을 사용하여 숫자가 아닌 모든 문자를 제거
    cleaned_value = re.sub(r'\D', '', value)
    # 문자열을 정수로 변환하여 반환
    return int(cleaned_value) if cleaned_value else 0

# 브라우저 드라이버 설정
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 1. 증권사 로그인 페이지 접속
url = 'https://www.ls-sec.co.kr/'
driver.get(url)

# 페이지 소스 확인을 위한 파일 저장 (디버깅용)
with open('data/ls-page0.html', 'w', encoding='utf-8') as file:
    file.write(driver.page_source)

try:
    # 2. 'goapplicationXnoti' iframe으로 전환
    driver.switch_to.frame('indexFrame')
    # iframe 내부의 페이지 소스 저장
    with open('data/ls-indexFrame.html', 'w', encoding='utf-8') as file:
        file.write(driver.page_source)

    print("iframe 내부의 소스를 저장했습니다.")
    # 4. '로그인' 링크를 기다리고 클릭
    login_element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//li[@class='login']/a"))
    )
    if not login_element:
        raise  Exception("로그인 링크를 찾을 수 없습니다.")
    
    print("로그인 링크가 나타났습니다. 클릭합니다.")
    login_element.click()
    # 첫 번째 프레임(index 0)으로 전환, 그리고 input#userId가 나타날 때까지 대기
    user_id_input = WebDriverWait(driver, 30).until(
        EC.frame_to_be_available_and_switch_to_it(0)  # 인덱스로 첫 번째 프레임 전환
    )
    
    # input#userId가 나타날 때까지 기다리기
    user_id_input = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input#userId"))
    )
    print("input#userId를 찾았습니다.")
    
    # 아이디 입력
    user_id_input.send_keys("kdy8017")
    
    # 비밀번호 입력란 찾기 및 비밀번호 입력
    passwd_input = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input#passwd"))
    )
    passwd_input.send_keys("8118kdy")
    
    # 로그인 프레임의 페이지 소스 저장
    with open('data/로그인프레임.html', 'w', encoding='utf-8') as file:
        file.write(driver.page_source)
    
    login_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.login_right a.btn_Login"))
    )
    login_button.click()
    print("로그인 버튼을 찾았습니다. 클릭합니다.")

    with open('data/로그인후.html', 'w', encoding='utf-8') as file:
        file.write(driver.page_source)
        
    time.sleep(5)    
    # 4. 로그인 버튼 클릭 후 새 창이 열리기 전 창 핸들 저장
    main_window = driver.current_window_handle
    all_windows = driver.window_handles

    # 5. 현재 열린 모든 창 핸들 목록
    print(f"모든 창 핸들: {all_windows}")

    # 6. 새 창이 열리면 팝업 창을 모두 닫음
    for handle in all_windows:
        if handle != main_window:
            driver.switch_to.window(handle)
            print(f"팝업 창 {handle}을 닫습니다.")
            driver.close()

    # 7. 다시 원래 메인 창으로 돌아옴
    driver.switch_to.window(main_window)
    #-------------------------------------------------------------------------
    
    # 로그아웃 찾기 
    driver.switch_to.frame('indexFrame')
    with open('data/로그인후_indexFrame.html', 'w', encoding='utf-8') as file:
        file.write(driver.page_source)  

    driver.execute_script("utilNavi(4);")
    print("utilNavi(4) 호출로 마이페이지로 이동했습니다.")
    time.sleep(5)
    with open('data/마이페이지.html', 'w', encoding='utf-8') as file:
        file.write(driver.page_source)  
    
    stock_balance_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='mypageSubAreaR']//div[@class='innerSubAreaR']//ul[@class='listTypeSub2']//a[@title='주식잔고']"))
    )
    if not stock_balance_link:
        raise  Exception("주식잔고 링크를 찾을 수 없습니다.")
    stock_balance_link.click()
    
    # 2. 비밀번호 필드 찾기 (id="passwd")
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "passwd"))
    )
    with open('data/주식잔고.html', 'w', encoding='utf-8') as file:
        file.write(driver.page_source)

    print("비밀번호 입력 필드를 찾았습니다.")    
    # 3. 비밀번호 입력 (예: 1234 입력)
    password_input.send_keys("8017") 
    password_input.send_keys(Keys.RETURN)
    
    message_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//p[@class='boxPara1' and text()='[00136]조회가 완료되었습니다.']"))
    )
    with open('data/주식잔고_Enter이후.html', 'w', encoding='utf-8') as file:
        file.write(driver.page_source)    
    print('-------------------------------------------------------------')
    print('테이블1의  값을 뽑아내다')    
    print('-------------------------------------------------------------')
    table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//table[@class='tbDataType1 tdRight tbMar4']"))
    )
    
    # 3. 테이블의 항목(헤더)와 값(데이터)을 추출
    headers = table.find_elements(By.XPATH, ".//th[@scope='col']")
    values = table.find_elements(By.XPATH, ".//td")
    
    # 4. 헤더와 값을 각각 추출하고 정리
    extracted_data = {}
    for i, header in enumerate(headers):
        header_text = header.text
        value_text = values[i].text
        # 불필요한 &nbsp;나 콤마 제거 후 정수로 변환
        cleaned_value = clean_value(value_text)
        extracted_data[header_text] = cleaned_value
    
    # 출력
    for key, value in extracted_data.items():
        print(f"{key}: {value}")    

    print('-------------------------------------------------------------')
    print('테이블2의  값을 뽑아내다')    
    print('-------------------------------------------------------------')
# 2. 테이블을 XPath로 찾음
    table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//table[@class='tbDataType1 th2Dep tdRight tbMar4']"))
    )

    # 3. 테이블에서 모든 행(tr) 가져오기
    rows = table.find_elements(By.XPATH, ".//tbody/tr")

    extracted_data = []
    
    # 4. 2개의 tr씩 묶어서 데이터 추출
    for i in range(0, len(rows), 2):
        first_row = rows[i].find_elements(By.TAG_NAME, 'td')  # 첫 번째 행 (종목명과 기본 정보)
        second_row = rows[i + 1].find_elements(By.TAG_NAME, 'td')  # 두 번째 행 (잔고구분과 추가 정보)
        
        # 5. 각 종목의 정보를 추출하여 딕셔너리로 저장
        stock_data = {
            "종목명": first_row[0].text.strip(),
            "결제잔고": clean_value(first_row[1].text),
            "미체결": clean_value(first_row[2].text),
            "현재가": clean_value(first_row[3].text),
            "평가금액": clean_value(first_row[4].text),
            "평가손익": clean_value(first_row[5].text),
            "대출금액": clean_value(first_row[6].text),
            "당일매수": clean_value(first_row[7].text),
            "전일매수": clean_value(first_row[8].text),
            "잔고구분": second_row[0].text.strip(),
            "보유수량": clean_value(second_row[1].text),
            "매도가능": clean_value(second_row[2].text),
            "평균단가": clean_value(second_row[3].text),
            "매입금액": clean_value(second_row[4].text),
            "수익률": second_row[5].text.strip(),  # 수익률은 퍼센트값이므로 문자를 그대로 사용
            "대출일": second_row[6].text.strip(),
            "당일매도": clean_value(second_row[7].text),
            "전일매도": clean_value(second_row[8].text)
        }

        # 6. 추출된 데이터를 리스트에 추가
        extracted_data.append(stock_data)

    # 출력
    for stock in extracted_data:
        print(stock)    
    print('-------------------------------------------------------------')
    print('로그아웃 버튼을 찾아서 클릭합니다.')
    print('-------------------------------------------------------------')
    #driver.switch_to.frame('indexFrame')
    # 4. '로그아웃' 링크를 기다리고 클릭
    logout_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//li[@class='login']/a[text()='로그아웃']"))
    )
    if not logout_button:
        raise  Exception("로그아웃 링크를 찾을 수 없습니다.")
    print(f"찾은 로그아웃text : {logout_button.text}")
    print("로그아웃 링크가 나타났습니다. 클릭합니다.")
    time.sleep(10)
    logout_button.click()
        
    
except Exception as e:
    print(f"오류 발생--->: {e}")
finally:
    # 기다렸다가 브라우저 닫기
    time.sleep(5)
    driver.quit()
