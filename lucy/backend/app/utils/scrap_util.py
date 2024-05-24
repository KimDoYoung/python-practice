import re
from datetime import datetime

def remove_non_numeric_chars(string) -> str:
    return re.sub(r'\D', '', string)

def to_ymd(str_date: str) -> str:
    ''' 날짜 문자열을 8자리 숫자로 변환 '''
    s = str_date.strip()
    if s == '':
        return ''
    s = remove_non_numeric_chars(s)
    if len(s) == 4:
        s =  str(datetime.now().year) + s
    return s

# 2024.06.05 ~ 06.07 -> sdate: 20240605, edate: 20240607
# 사용법 : sdate, edate = extract_dates(pattern)
def extract_dates(date_range_str: str, gubun: str = "~"):

    split_pattern = r'\s*' + re.escape(gubun) + r'\s*'
    
    # 패턴을 split_pattern으로 분할
    parts = re.split(split_pattern, date_range_str.strip())
    parts = [remove_non_numeric_chars(part) for part in parts]
    
    if len(parts[1]) == 4:
        parts[1] = parts[0][:4] + parts[1]

    return parts[0], parts[1]

# 1,000 ~ 2,000 -> scost: 1000, ecost: 2000
def extract_numbers(cost_range : str, gubun: str = "~"):
    if cost_range.strip() == '':
        return None, None
    # 숫자와 '~' 주변의 공백을 포함하여 패턴 분할
    split_pattern = r'\s*' + re.escape(gubun) + r'\s*'
    
    # 패턴을 split_pattern으로 분할
    parts = re.split(split_pattern, cost_range.strip())
    if len(parts) == 1:
        return int(remove_non_numeric_chars(parts[0])), int(remove_non_numeric_chars(parts[0]))
    parts = [remove_non_numeric_chars(part) for part in parts]
    
    return int(parts[0]), int(parts[1])


# print(_fmt_number_kor(1234567890))  # 출력 예: 일십이억삼천사백오십육만칠천팔백구십원
def fmt_number_kor(val):
    num_kor = ["", "일", "이", "삼", "사", "오", "육", "칠", "팔", "구", "십"]
    dan_kor = ["", "십", "백", "천", "", "십", "백", "천", "", "십", "백", "천", "", "십", "백", "천"]
    result = ""
    
    if val is not None and isinstance(val, int):
        val_str = str(val)
        length = len(val_str)
        
        for i in range(length):
            str_piece = ""
            num = num_kor[int(val_str[length - (i + 1)])]
            if num != "":
                str_piece += num + dan_kor[i]
            if i == 4:
                str_piece += "만"
            elif i == 8:
                str_piece += "억"
            elif i == 12:
                str_piece += "조"
            
            result = str_piece + result
        
        # 불필요 단위 제거
        result = result.replace("억만", "억").replace("조만", "조").replace("조억", "조")
        
        result += "원"
    
    return result

# print(get_korean_number(1234 567890123))  # 예시 출력: 1,234억5,678만9,0123
def get_korean_number1(number):
    korean_units = ['兆', '億', '萬', '']
    unit = 10000
    answer = ''
    
    while number > 0:
        mod = number % unit
        # mod를 세 자리 단위로 쉼표를 찍어 문자열로 만듬
        mod_to_string = f"{mod:,}"
        number = number // unit
        answer = f"{mod_to_string}{korean_units.pop()}{answer}"
    
    return answer

#print(get_korean_number(1234567890123))  # 예시 출력: 일조 이천삼백사십오억 육천칠백팔십구만 천이백삼십삼
def get_korean_number2(number):
    korean_number = ['', '일', '이', '삼', '사', '오', '육', '칠', '팔', '구']
    ten_unit = ['', '십', '백', '천']
    ten_thousand_unit = ['兆', '億', '萬', '']
    unit = 10000
    answer = ''
    
    while number > 0:
        mod = number % unit
        mod_to_array = list(str(mod))
        length = len(mod_to_array) - 1

        mod_to_korean = ''
        for index, value in enumerate(mod_to_array):
            value_to_number = int(value)
            if value_to_number == 0:
                continue
            # '십', '백', '천' 등의 단위 앞에 '일'이 오면 생략
            number_to_korean = '' if (index < length and value_to_number == 1) else korean_number[value_to_number]
            mod_to_korean += number_to_korean + ten_unit[length - index]
        
        answer = f"{mod_to_korean}{ten_thousand_unit.pop()} {answer}".strip()
        number = number // unit
    
    return answer.strip()

def to_num(s: str) -> int:
    '''주식수 문자열을 정수로 변환'''
    if s == '':
        return None
    s1 = s.strip()
    return int(remove_non_numeric_chars(s1))

def to_won(amount_str):
    ''' 금액 문자열을 정수(금액 원)로 변환 '''
    # 백만원 단위 처리
    if '백만원' in amount_str:
        clean_str = re.sub(r'[^0-9.]', '', amount_str)
        if clean_str:  # clean_str이 비어있지 않은 경우에만 변환
            return int(float(clean_str) * 1000000)
        else:
            return None  # 유효하지 않은 문자열인 경우 None 반환
    
    # 숫자와 점(.)을 제외한 모든 문자 제거
    clean_str = re.sub(r'[^0-9.]', '', amount_str)
    if clean_str:  # clean_str이 비어있지 않은 경우에만 변환
        return int(float(clean_str))
    else:
        return None  # 유효하지 않은 문자열인 경우 None 반환



def extract_competition_rates(s: str):
    '''경쟁률 문자열에서 경쟁률과 비례 경쟁률을 추출'''
    if s == '':
        return None, None
    # 정규 표현식을 사용하여 첫 번째 비율 추출
    primary_ratio_match = re.search(r'([\d,]+\.\d+):1', s)
    if primary_ratio_match:
        primary_ratio = float(primary_ratio_match.group(1).replace(',', ''))
    else:
        primary_ratio = None
    
    # 정규 표현식을 사용하여 비례 비율 추출
    proportional_ratio_match = re.search(r'비례 ([\d,]+):1', s)
    if proportional_ratio_match:
        proportional_ratio = float(proportional_ratio_match.group(1).replace(',', ''))
    else:
        proportional_ratio = None
    
    return primary_ratio, proportional_ratio

def extract_stock_and_limit(s):
    '''주식수 청약한도 추출'''
    stock_match = re.search(r'주식수: ([0-9,~,]+) 주', s)
    stock = stock_match.group(1) if stock_match else ''
    
    # 청약한도 추출
    limit_match = re.search(r'청약한도: ([0-9,~,]+) 주', s)
    limit = limit_match.group(1) if limit_match else ''
    
    # 주식수 및 청약한도 범위 처리
    if '~' not in stock:
        stock = f'{int(stock.replace(",", "")):,}~{int(stock.replace(",", "")):,}'
    if limit:
        if '~' not in limit:
            limit = f'{int(limit.replace(",", "")):,}~{int(limit.replace(",", "")):,}'
    else:
        limit = None    
    return stock, limit

