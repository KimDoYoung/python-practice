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

    # 기업개요: summary_info 클래스 내부의 모든 <p> 태그를 찾음
    summary_info = soup.find('div', class_='summary_info')
    paragraphs = summary_info.find_all('p')
    
    # <p> 태그 내용을 줄바꿈과 함께 합침
    company_summary = "\n".join(p.get_text(strip=True) for p in paragraphs)


    stock_info = {
        'stk_code': stk_code,
        'stk_name': stk_name,
        'company_summary': company_summary
    }
    return stock_info