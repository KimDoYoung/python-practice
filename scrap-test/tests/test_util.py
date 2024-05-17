import pytest
from util import extract_competition_rates, fmt_number_kor, to_num
from util import fmt_number_kor, extract_dates
from util import extract_numbers
from util import to_won

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
    assert to_num(1) == 1

def test_to_won():
    assert to_won('2,567 (백만원)') == 2567000000
    assert to_won('2,000원') == 2000
    assert to_won('1,162,640,000') == 1162640000
    assert None == to_won('- (백만원)') 
    assert None == to_won('-')

def test_extract_competition_rates():
    assert 2071.41,4143.0 == extract_competition_rates("2071.41:1 (비례 4143:1)")
    assert 2071.41,None  == extract_competition_rates("2071.41:1 ")