from backend.app.utils.naver_util import get_stock_info


def test_get_stock_info():
    stk_code = '005930'
    info = get_stock_info(stk_code)
    print(info)
