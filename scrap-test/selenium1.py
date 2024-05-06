from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

service = Service('./chromedriver.exe')

driver = webdriver.Chrome(service=service)

driver.get('https://www.google.com')
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'q')))

