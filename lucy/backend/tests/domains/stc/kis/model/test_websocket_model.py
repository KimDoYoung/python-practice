
import pytest
from backend.app.domains.stc.kis.model.websocket_model import KisWsResponse


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
    