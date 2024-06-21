import pytest
from backend.app.domains.stc.kis.model.websocket_model import H0STASP0, H0STCNI0, H0STCNT0, KisWsResponse


def test_create():
    # JSON 데이터 예시
    json_data = '{"header":{"tr_id":"H0STASP0","tr_key":"005930","encrypt":"N"},"body":{"rt_cd":"0","msg_cd":"OPSP0000","msg1":"SUBSCRIBE SUCCESS","output":{"iv":"d59d91fcf9fd0044","key":"iuheqrmvfxoceaxeyqgjwesozgizmmgx"}}}'

    kis_ws_response_model = KisWsResponse.from_json_str(json_data)
    
    # 객체의 속성 검증
    assert kis_ws_response_model.header.tr_id == "H0STASP0"
    assert kis_ws_response_model.header.tr_key == "005930"
    assert kis_ws_response_model.header.encrypt == "N"
    assert kis_ws_response_model.body.rt_cd == "0"
    assert kis_ws_response_model.body.msg_cd == "OPSP0000"
    assert kis_ws_response_model.body.msg1 == "SUBSCRIBE SUCCESS"
    assert kis_ws_response_model.body.output.iv == "d59d91fcf9fd0044"
    assert kis_ws_response_model.body.output.key == "iuheqrmvfxoceaxeyqgjwesozgizmmgx"

    wrong_json_data = '{"header1":{"tr_id":"H0STASP0","tr_key":"005930","encrypt":"N"},"body":{"rt_cd":"0","msg_cd":"OPSP0000","msg1":"SUBSCRIBE SUCCESS","output":{"iv":"d59d91fcf9fd0044","key":"iuheqrmvfxoceaxeyqgjwesozgizmmgx"}}}'

    with pytest.raises(ValueError):
        kis_ws_response_model = KisWsResponse.from_json_str(wrong_json_data)

# 실시간 호가 
def test_hoga():
    # 데이터 예시
    data_str = """
    005930^153948^0^80100^80200^80300^80400^80500^80600^80700^80800^80900^81000^80000^79900^79800^79700^79600^79500^79400^79300^79200^79100^77855^73175^72845^706^4642^68925^67828^50635^85021^157328^481698^238211^173635^103434^135417^163796^50590^43877^34519^43445^658960^1468622^9635^88360^0^0^3292594^-81600^5^-100.00^16873825^0^0^-19^0^0
    """

    # Pydantic 모델로 변환
    h0 = H0STASP0.from_text(data_str)
    
    assert h0 is not None

    # 데이터 출력
    print(f"유가증권 단축 종목코드 [{h0.단축종목코드}]")
    print(f"영업시간 [{h0.영업시간}] 시간구분코드 [{h0.시간구분코드}]")
    print("======================================")
    for i in range(10):
        print(f"매도호가배열{10-i:02} [{h0.매도호가배열[i].가격}]    잔량{10-i:02} [{h0.매도호가배열[i].잔량}]")
    print("--------------------------------------")
    for i in range(10):
        print(f"매수호가배열{i+1:02} [{h0.매수호가배열[i].가격}]    잔량{i+1:02} [{h0.매수호가배열[i].잔량}]")
    print("======================================")
    print(f"총매도호가 잔량        [{h0.총매도호가_잔량}]")
    print(f"총매도호가 잔량 증감   [{h0.총매도호가_잔량_증감}]")
    print(f"총매수호가 잔량        [{h0.총매수호가_잔량}]")
    print(f"총매수호가 잔량 증감   [{h0.총매수호가_잔량_증감}]")
    print(f"시간외 총매도호가 잔량 [{h0.시간외_총매도호가_잔량}]")
    print(f"시간외 총매수호가 잔량 [{h0.시간외_총매수호가_잔량}]")
    print(f"시간외 총매도호가 잔량 증감 [{h0.시간외_총매도호가_잔량_증감}]")
    print(f"시간외 총매수호가 잔량 증감 [{h0.시간외_총매수호가_잔량_증감}]")
    print(f"예상 체결가            [{h0.예상_체결가}]")
    print(f"예상 체결량            [{h0.예상_체결량}]")
    print(f"예상 거래량            [{h0.예상_거래량}]")
    print(f"예상체결 대비          [{h0.예상_체결_대비}]")
    print(f"예상체결 대비부호      [{h0.예상_체결_대비부호}]")
    print(f"예상체결 전일대비율    [{h0.예상_체결_전일대비율}]")
    print(f"누적거래량             [{h0.누적_거래량}]")
    print(f"주식매매 구분코드      [{h0.주식매매_구분코드}]")


# 실시간 체결가 
def test_purchase():
    # 예시 데이터
    data_str = "005930^093354^71900^5^-100^-0.14^72023.83^72100^72400^71700^71900^71800^1^3052507^219853241700^5105^6937^1832^84.90^1366314^1159996^1^0.39^20.28^090020^5^-200^090820^5^-500^092619^2^200^20230612^20^N^65945^216924^1118750^2199206^0.05^2424142^125.92^0^^72100"
    # Pydantic 모델로 변환
    purchase = H0STCNT0.from_text(data_str)
    assert isinstance(purchase, H0STCNT0)
    assert purchase is not None
    assert purchase.유가증권_단축_종목코드 == "005930"

# 실시간 체결통보
def test_purchase_notice():
    text_data = "ID123456^ACC9876543210^ORDER12345^ORDER54321^01^1^00^1^ABC123456^100^1000^120000^0^2^1^BR001^200^계좌명123^종목명123^02^20220101^종목명12345678901234567890^1500"
    h0 = H0STCNI0.from_text(text_data)
    assert isinstance(h0, H0STCNI0)
    assert h0.고객_ID == "ID123456"
    assert h0.주문가격 == "1500"