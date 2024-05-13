from util import fmt_number_kor
from util import fmt_number_kor, extract_dates
from util import extract_numbers

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
    assert start == '11000'
    assert end == '14000'