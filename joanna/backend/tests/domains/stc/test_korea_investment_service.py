import pytest
from backend.app.domains.stc.korea_investment.korea_investment_service import get_access_token, get_hashkey, get_market_price

@pytest.mark.skip(reason="Ignore this test")
def test_accesskey_not_null():
    accesskey = get_access_token()
    assert accesskey is not None

@pytest.mark.skip(reason="Ignore this test")
def test_hash_code():
    datas = {
        "CANO": '00000000',
        "ACNT_PRDT_CD": "01",
        "OVRS_EXCG_CD": "SHAA",
        "PDNO": "00001",
        "ORD_QTY": "500",
        "OVRS_ORD_UNPR": "52.65",
        "ORD_SVR_DVSN_CD": "0"
    }
    hashkey = get_hashkey(datas)
    assert hashkey is not None
    
@pytest.mark.skip(reason="Ignore this test")
def test_market_price():
    json = get_market_price("J","005930")
    print(json)
    assert json != {}

