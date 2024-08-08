# hoga_datas.py
"""
모듈 설명: 
    - DantaWsManager에서 사용하는 것으로 호가 데이터를 관리하는 클래스
    - 각 stk_code별로 dataframe을 갖고 있다.
주요 기능:
    - 

작성자: 김도영
작성일: 2024-08-08
버전: 1.0
"""
import pandas as pd
from collections import defaultdict

class HogaDatas:
    def __init__(self, max_length=100):
        # 각 종목 코드를 key로 하고 DataFrame을 value로 하는 딕셔너리
        self.data = defaultdict(pd.DataFrame)
        self.max_length = max_length  # 각 DataFrame의 최대 행 수

    def append(self, message: str):
        # 로그에서 받은 문자열 message를 파싱하여 데이터 추가
        try:
            # 필요한 데이터 추출
            parts = message.split('|')
            data_str = parts[-1]
            data_dict = eval(data_str)  # 문자열을 딕셔너리로 변환 (주의: eval은 보안 위험이 있으므로 안전한 방법으로 변경 필요)
            
            stk_code = data_dict['MKSC_SHRN_ISCD']
            df = pd.DataFrame([data_dict])

            if stk_code in self.data:
                self.data[stk_code] = pd.concat([self.data[stk_code], df], ignore_index=True)
                # 최대 길이를 초과하면 오래된 데이터 삭제
                if len(self.data[stk_code]) > self.max_length:
                    self.data[stk_code] = self.data[stk_code].iloc[-self.max_length:]
            else:
                self.data[stk_code] = df
        except Exception as e:
            print(f"Error parsing message: {e}")

    def get_sell_stk_codes(self):
        SOME_THRESHOLD = 1000
        # 매도 기준에 적합한 종목 코드 배열 반환
        sell_stk_codes = []
        for stk_code, df in self.data.items():
            # 예: ASKP1 값이 특정 기준 이상인 종목 코드 추가
            if not df.empty and df.iloc[-1]['ASKP1'] > SOME_THRESHOLD:
                sell_stk_codes.append(stk_code)
        return sell_stk_codes

    def save_to_excel(self, file_path: str):
        # 모든 데이터를 종목 코드별로 엑셀 파일에 저장
        with pd.ExcelWriter(file_path) as writer:
            for stk_code, df in self.data.items():
                df.to_excel(writer, sheet_name=stk_code)

    def clear(self):
        # 모든 데이터 삭제
        self.data.clear()