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