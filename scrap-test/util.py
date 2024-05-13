import re

# 2024.06.05 ~ 06.07 -> sdate: 20240605, edate: 20240607
# 사용법 : sdate, edate = extract_dates(pattern)
def extract_dates(pattern):
    # 날짜 패턴: YYYY.MM.DD
    date_pattern = r'(\d{4}\.\d{2}\.\d{2})'
    # '~'와 주변 공백을 포함하여 패턴 분할
    split_pattern = r'\s*~\s*'
    
    # 패턴을 split_pattern으로 분할
    parts = re.split(split_pattern, pattern)
    
    # 날짜 추출
    dates = re.findall(date_pattern, pattern)
    
    # 분할된 부분과 날짜 추출을 바탕으로 sdate와 edate 결정
    if len(parts) == 2:
        sdate = dates[0].replace('.', '') if dates and parts[0] else ""
        edate = dates[1].replace('.', '') if len(dates) > 1 else dates[0].replace('.', '') if len(dates) == 1 and parts[1] else ""
    elif len(parts) == 1:
        # 하나의 날짜만 있는 경우
        sdate = dates[0].replace('.', '') if dates else ""
        edate = ""
    else:
        sdate = ""
        edate = ""

    return sdate, edate

# 1,000 ~ 2,000 -> scost: 1000, ecost: 2000
def extract_costs(pattern):
    # 숫자와 '~' 주변의 공백을 포함하여 패턴 분할
    split_pattern = r'\s*~\s*'
    
    # 패턴을 split_pattern으로 분할
    parts = re.split(split_pattern, pattern)
    
    # 각 부분에서 콤마를 제거하고 숫자만 추출
    scost = parts[0].replace(',', '') if parts[0] else ""
    ecost = parts[1].replace(',', '') if len(parts) > 1 and parts[1] else ""

    return scost, ecost


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

# 테스트 코드

