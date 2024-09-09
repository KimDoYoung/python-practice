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
def get_name_by_code(code: str):
    '''주식 코드로부터 주식 이름을 가져온다.'''
    stock_info = get_stock_info(code)
    if stock_info['stk_name'] is not None:
        return stock_info['stk_name']
    else:
        return None

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

    # 필요한 div 컨테이너를 먼저 찾아서 그 안에서 작업
    container_div = soup.find('div', id='tab_con1', class_='tab_con1')
    
    # 시가총액
    market_cap = container_div.find('th', text='시가총액').find_next('td').get_text(separator='').strip()

    # 시가총액순위
    market_cap_rank = container_div.find('a', text='시가총액순위').find_next('td').get_text(separator='').strip()

    # 상장주식수
    num_of_shares = container_div.find('th', text='상장주식수').find_next('td').get_text(separator='').strip()

    stock_info = {
        'stk_code': stk_code,
        'stk_name': stk_name,
        'company_summary': company_summary,
        'market_cap': market_cap,
        'market_cap_rank': market_cap_rank,
        'num_of_shares': num_of_shares,
    }
    return stock_info