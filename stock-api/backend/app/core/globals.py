# globals.py
"""
모듈 설명: 
    - Manager들을 전역변수로 관리하는 모듈
주요 기능:
    - Manager들을 전역변수로 관리
    - 기타 전역변수를 관리

작성자: 김도영
작성일: 04
버전: 1.0
"""
# client 즉 AssetErp와 통신하는 WebSocketManager
client_ws_manager = None

# KIS,LS 등 증권사의 체결통보(실시간)를 받기위한 WebSocketManager
stock_ws_manager = None

# 각 증권사들의  주식 API를 통합적으로 관리하는 Manager
api_manager = None