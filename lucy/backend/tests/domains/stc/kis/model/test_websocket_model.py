
import pytest
from backend.app.domains.stc.kis.model.websocket_model import H0STASP0, KisWsResponse


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

def test_hoga():
    # 데이터 예시
    data_str = """
    005930^153948^0^80100^80200^80300^80400^80500^80600^80700^80800^80900^81000^80000^79900^79800^79700^79600^79500^79400^79300^79200^79100^77855^73175^72845^706^4642^68925^67828^50635^85021^157328^481698^238211^173635^103434^135417^163796^50590^43877^34519^43445^658960^1468622^9635^88360^0^0^3292594^-81600^5^-100.00^16873825^0^0^-19^0^0
    """

    # Pydantic 모델로 변환
    quote_data = H0STASP0.from_text(data_str)

    # 데이터 출력
    print(f"유가증권 단축 종목코드 [{quote_data.단축종목코드}]")
    print(f"영업시간 [{quote_data.영업시간}] 시간구분코드 [{quote_data.시간구분코드}]")
    print("======================================")
    for i in range(10):
        print(f"매도호가{10-i:02} [{quote_data.매도호가[i].가격}]    잔량{10-i:02} [{quote_data.매도호가[i].잔량}]")
    print("--------------------------------------")
    for i in range(10):
        print(f"매수호가{10-i:02} [{quote_data.매수호가[i].가격}]    잔량{10-i:02} [{quote_data.매수호가[i].잔량}]")
    print("======================================")
    print(f"총매도호가 잔량        [{quote_data.총매도호가_잔량}]")
    print(f"총매도호가 잔량 증감   [{quote_data.총매도호가_잔량_증감}]")
    print(f"총매수호가 잔량        [{quote_data.총매수호가_잔량}]")
    print(f"총매수호가 잔량 증감   [{quote_data.총매수호가_잔량_증감}]")
    print(f"시간외 총매도호가 잔량 [{quote_data.시간외_총매도호가_잔량}]")
    print(f"시간외 총매수호가 잔량 [{quote_data.시간외_총매수호가_잔량}]")
    print(f"시간외 총매도호가 잔량 증감 [{quote_data.시간외_총매도호가_잔량_증감}]")
    print(f"시간외 총매수호가 잔량 증감 [{quote_data.시간외_총매수호가_잔량_증감}]")
    print(f"예상 체결가            [{quote_data.예상_체결가}]")
    print(f"예상 체결량            [{quote_data.예상_체결량}]")
    print(f"예상 거래량            [{quote_data.예상_거래량}]")
    print(f"예상체결 대비          [{quote_data.예상_체결_대비}]")
    print(f"예상체결 대비부호      [{quote_data.예상_체결_대비부호}]")
    print(f"예상체결 전일대비율    [{quote_data.예상_체결_전일대비율}]")
    print(f"누적거래량             [{quote_data.누적_거래량}]")
    print(f"주식매매 구분코드      [{quote_data.주식매매_구분코드}]")