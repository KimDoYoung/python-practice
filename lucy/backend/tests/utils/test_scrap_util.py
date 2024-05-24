import pytest
from backend.app.utils.scrap_util import extract_competition_rates, extract_stock_and_limit, fmt_number_kor, to_num
from backend.app.utils.scrap_util import fmt_number_kor, extract_dates
from backend.app.utils.scrap_util import extract_numbers
from backend.app.utils.scrap_util import to_won

def test_addition():
    k = fmt_number_kor(123)
    assert k == '일백이십삼원'
    k = fmt_number_kor(1234)
    assert k == '일천이백삼십사원'
    k = fmt_number_kor(12345)
    assert k == '일만이천삼백사십오원'
    k = fmt_number_kor(123456)
    assert k == '일십이만삼천사백오십육원'

def test_extract_dates():
    s = '2024.03.18~03.19'
    start, end = extract_dates(s)
    assert start == '20240318'
    assert end == '20240319'

    s = '2024.03.18 ~ 2024.03.19'
    start, end = extract_dates(s)
    assert start == '20240318'
    assert end == '20240319'

def test_extract_numbers():
    s="11,000~14,000"    
    start, end = extract_numbers(s)
    assert start == 11000
    assert end == 14000

    s="1,500,000 주"    
    start, end = extract_numbers(s)
    assert start == 1500000
    assert end == 1500000

    start, end = extract_numbers('')
    assert start == None
    assert end == None


def test_to_num():
    assert to_num('1') == 1

def test_to_won():
    assert to_won('2,567 (백만원)') == 2567000000
    assert to_won('2,000원') == 2000
    assert to_won('1,162,640,000') == 1162640000
    assert None == to_won('- (백만원)') 
    assert None == to_won('-')

def test_extract_competition_rates():
    v1, v2 = extract_competition_rates("2071.41:1 (비례 4143:1)")
    assert v1 == 2071.41
    assert v2 == 4143.0
    v1, v2 = extract_competition_rates("2,071.41:1 (비례 4,143:1)")
    assert v1 == 2071.41
    assert v2 == 4143.0
    v1, v2 = extract_competition_rates("2071.41:1 ")
    assert v1 == 2071.41
    assert v2 == None
    v1, v2 = extract_competition_rates("2,071.41:1")
    assert v1 == 2071.41
    assert v2 == None
    

# 주식수: 1,306,000~1,567,200 주 \xa0\xa0/\xa0\xa0 청약한도: 130,000 주    

def test_extract_stock_and_limit():
    s = '주식수: 1,306,000~1,567,200 주 \xa0\xa0/\xa0\xa0 청약한도: 130,000 주'
    start, end = extract_stock_and_limit(s)
    assert start == '1,306,000~1,567,200'
    assert end == '130,000~130,000'

    s = '주식수: 350,000~420,000 주 &nbsp;&nbsp;/&nbsp;&nbsp; 청약한도: 12,000~14,000 주'
    start, end = extract_stock_and_limit(s)
    assert start == '350,000~420,000'
    assert end == '12,000~14,000'

    s = '주식수: 1,500,000 주   /   청약한도: 50,000 주'
    start, end = extract_stock_and_limit(s)
    assert start == '1,500,000~1,500,000'
    assert end == '50,000~50,000'

    s = '주식수: 1,000,000~1,200,000 주 &nbsp;&nbsp;/&nbsp;&nbsp; 청약한도: - 주'
    start, end = extract_stock_and_limit(s)
    assert start == '1,000,000~1,200,000'
    assert end == None

    

def test_1():
    assert 1 == 1
