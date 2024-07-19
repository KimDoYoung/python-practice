# misc_util.py
"""
모듈 설명: 
    - 자잘한 유틸리티 함수들
주요 기능:
    - get_today : 오늘 날짜를 반환한다.
    - only_number : 문자열에서 숫자만 추출

작성자: 김도영
작성일: 2024-07-19
버전: 1.0
"""
from datetime import datetime


def get_today():
    ''' 오늘 날짜를 반환한다. '''
    yoils = ["월", "화", "수", "목", "금", "토", "일"]
    yoil = datetime.now().weekday()
    yoil_korean = yoils[yoil]
    today = datetime.now().strftime("%Y-%m-%d")
    today = f"{today}({yoil_korean})"
    return today

def only_number(s:str):
    ''' 숫자만 추출 '''
    return ''.join(filter(str.isdigit, s))