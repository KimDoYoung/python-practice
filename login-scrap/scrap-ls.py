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
    if login_element:
        print("로그인 링크가 나타났습니다. 클릭합니다.")
        login_element.click()
        time.sleep(5)

        # 2. 모든 iframe 탐색
        frames = driver.find_elements(By.TAG_NAME, "iframe")
        print(f"총 {len(frames)}개의 프레임을 찾았습니다.")
        found_user_id = False

        for index, frame in enumerate(frames):
            # 프레임 속성 출력
            frame_id = frame.get_attribute("id")
            frame_name = frame.get_attribute("name")
            frame_src = frame.get_attribute("src")
            
            print(f"{index+1}/{len(frames)} 번째 프레임 탐색 중...")
            print(f"Frame ID: {frame_id}, Frame Name: {frame_name}, Frame Src: {frame_src}")            
            # 각 프레임으로 전환
            driver.switch_to.frame(index)
            # 각 프레임의 소스를 저장
            with open(f'data/login-frame-{index}.html', 'w', encoding='utf-8') as file:
                file.write(driver.page_source)
            print(f"{index+1}/{len(frames)} 번째 프레임에서 탐색 중...")
            try:
                # input#userId 요소 찾기
                user_id_input = driver.find_element(By.CSS_SELECTOR, "input#userId")
                if user_id_input:
                    print("input#userId를 찾았습니다.")
                    user_id_input.send_keys("kdy8017")
                    found_user_id = True
                    break
            except Exception as e:
                print(f"input#userId 탐색 중 오류 발생: {e}")        
        
            # 프레임에서 빠져나오기
            driver.switch_to.default_content()
        if found_user_id:
            passwd_input = driver.find_element(By.CSS_SELECTOR, "input#passwd")
            if passwd_input:
                passwd_input.send_keys("8118kdy")
                passwd_input.submit()
                print("로그인 완료.")        
            
        # # userId 필드를 찾아 값을 입력
        # user_id_element = WebDriverWait(driver, 30).until(
        #     EC.presence_of_element_located((By.ID, "userId"))
        # )
        # user_id_element.clear()  # 기존 값이 있을 경우 지움
        # user_id_element.send_keys('kdy8017')  # 아이디 입력

        # # passwd 필드를 찾아 값을 입력
        # passwd_element = WebDriverWait(driver, 30).until(
        #     EC.presence_of_element_located((By.ID, "passwd"))
        # )
        # passwd_element.clear()  # 기존 값이 있을 경우 지움
        # passwd_element.send_keys('8118kdy')  # 비밀번호 입력

        # # 비밀번호 필드에서 엔터 키를 눌러 로그인 실행
        # passwd_element.send_keys(Keys.ENTER)

        print("로그인 시도 중...")
        
    else:
        print("로그인 링크를 찾을 수 없습니다.")    

    # 3. 로그인 버튼이 나올 때까지 대기 (CSS 선택자로 로그인 링크 찾기)
    # login_element = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CSS_SELECTOR, "li.login a"))
    # )
    
    # if login_element:
    #     login_element.click()
    #     print("로그인 링크가 나타났습니다.")
    # else:
    #     print("로그인 링크를 찾을 수 없습니다.")
except Exception as e:
    print(f"로그인 링크를 기다리는 중 오류 발생: {e}")
finally:
    # 기다렸다가 브라우저 닫기
    time.sleep(5)
    driver.quit()
