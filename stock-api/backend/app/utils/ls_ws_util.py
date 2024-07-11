from enum import StrEnum
import json
from typing import Union


from backend.app.domains.stc.ls.model.ls_websocket_model import NewsResponse, Sc1Response
from backend.app.domains.stc.ls.model.ls_ws_request_model import Body, Header, LsWsRequest


class LS_WSReq(StrEnum):
    뉴스 = '뉴스'   # News
    주식주문체결 = '주식주문체결'  # 


def new_ls_ws_request()->LsWsRequest:
    return LsWsRequest(
        header=Header(
            token="",
            tr_type=""
        ),
        body=Body(
            tr_cd="",
            tr_key=""
        )
    )

def ls_ws_response_factory(received_text: str) -> Union[NewsResponse, Sc1Response]:
    data = json.loads(received_text)
    tr_cd = data['header']['tr_cd']
    
    if tr_cd == 'NWS':
        return NewsResponse(**data)
    elif tr_cd == 'SC1':
        return Sc1Response(**data)
    else:
        raise ValueError(f"Unknown tr_cd: {tr_cd}")