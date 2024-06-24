from backend.app.domains.stc.kis.model.kis_ws_request_model import Body, Header, Input, KisWsRequest


def is_real_data(txt: str) -> bool:
    return txt[0] == '0' or txt[0] == '1'

def real_data_trid(txt: str) -> str:
    return txt.split('|')[1]

def new_kis_ws_request() -> KisWsRequest:
    return KisWsRequest(
        header=Header(
            approval_key="",
            personalseckey="",
            custtype="P",
            tr_type="",
            content_type="utf-8"
        ),
        body=Body(
            input=Input(
                tr_id="",
                tr_key=""
            )
        )
    )
