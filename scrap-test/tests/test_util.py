from util import fmt_number_kor

def test_addition():
    k = fmt_number_kor(123)
    assert k == '일백이십삼원'
    k = fmt_number_kor(1234)
    assert k == '일천이백삼십사원'
    k = fmt_number_kor(12345)
    assert k == '일만이천삼백사십오원'
    k = fmt_number_kor(123456)
    assert k == '일십이만삼천사백오십육원'
