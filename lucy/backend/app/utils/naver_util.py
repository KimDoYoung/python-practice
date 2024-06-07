# naver_util.py
"""
모듈 설명: 
    - 네이버증권에서 정보를 가져온다.
주요 기능:
    -   기능을 넣으시오

작성자: 김도영
작성일: 07
버전: 1.0
"""

from bs4 import BeautifulSoup
import requests



def get_stock_info(stk_code: str):
    '''주식 코드로부터 주식 정보를 가져온다.'''
    page = requests.get(f"https://finance.naver.com/item/main.nhn?code={stk_code}")
    soup = BeautifulSoup(page.text, 'html.parser')
    div_class_name = 'wrap_company'
    stk_name = soup.select_one(f'div.{div_class_name} h2 a').text

    stock_info = {
        'stk_code': stk_code,
        'stk_name': stk_name,
    }
    return stock_info