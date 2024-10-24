import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

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
    
    
    time.sleep(5)
    with open('data/주식잔고.html', 'w', encoding='utf-8') as file:
        file.write(driver.page_source)
    time.sleep(5)
    driver.switch_to.frame('indexFrame')
    # 4. '로그아웃' 링크를 기다리고 클릭
    logout_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//li[@class='login']/a[text()='로그아웃']"))
    )
    if not logout_button:
        raise  Exception("로그아웃 링크를 찾을 수 없습니다.")
    print(f"찾은 로그아웃text : {logout_button.text}")
    print("로그아웃 링크가 나타났습니다. 클릭합니다.")
    time.sleep(30)
    logout_button.click()
        
    
except Exception as e:
    print(f"오류 발생--->: {e}")
finally:
    # 기다렸다가 브라우저 닫기
    time.sleep(5)
    driver.quit()
