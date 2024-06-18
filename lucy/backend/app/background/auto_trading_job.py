# auto_trading_job.py
"""
모듈 설명: 
    - 자동으로 단타매매를 한다.
주요 기능:
    - 1. 조건식으로 오늘 단타를 칠 목록을 가져온다.
    - 2. 실시간으로 호가 및 체결가를 가져온다.
    - 3. 호가 및 체결가를 분석하여 매수/매도를 한다.

작성자: 김도영
작성일: 18
버전: 1.0
"""

# 전역 변수 설정
auto_trading_running = False
auto_trading_thread = None

def job1():
    global auto_trading_running
    while auto_trading_running:
        print("작업 수행 중...")
        time.sleep(1)  # 실제 작업을 대체하는 지연