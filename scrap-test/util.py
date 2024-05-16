import re

def remove_non_numeric_chars(string):
    return re.sub(r'\D', '', string)

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
def extract_numbers(cost_range: str, gubun: str = "~"):
    # 숫자와 '~' 주변의 공백을 포함하여 패턴 분할
    split_pattern = r'\s*' + re.escape(gubun) + r'\s*'
    
    # 패턴을 split_pattern으로 분할
    parts = re.split(split_pattern, cost_range.strip())
    parts = [remove_non_numeric_chars(part) for part in parts]
    
    return parts[0], parts[1]


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

def to_won(amount_str):
    ''' 금액 문자열을 정수(금액 원)로 변환 '''
    # 백만원 단위 처리
    if '백만원' in amount_str:
        clean_str = re.sub(r'[^0-9.]', '', amount_str)
        if clean_str:  # clean_str이 비어있지 않은 경우에만 변환
            return int(float(clean_str) * 1000000)
        else:
            raise ValueError(f"Invalid amount string: '{amount_str}'")
    
    # 숫자와 점(.)을 제외한 모든 문자 제거
    clean_str = re.sub(r'[^0-9.]', '', amount_str)
    if clean_str:  # clean_str이 비어있지 않은 경우에만 변환
        return int(float(clean_str))
    else:
        raise ValueError(f"Invalid amount string: '{amount_str}'")

