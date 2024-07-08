from backend.app.domains.stc.common_model import OrderCash_Request
from backend.app.domains.stc.ls.model.cspat00601_model import CSPAT00601_Request, CSPAT00601InBlock1


def order_cash_to_cspat00601_Request(order: OrderCash_Request) -> CSPAT00601_Request:
    '''LS 현물주문 요청 모델로 변환'''
    bns_tp_code = '2' if order.buy_sell_gb == '매수' else '1'
    ord_prc = float(order.cost) if order.cost > 0 else 0.0
    ordprc_ptn_code = '00' if order.cost > 0 else '03'

    in_block = CSPAT00601InBlock1(
        IsuNo=order.stk_code,
        OrdQty=order.qty,
        OrdPrc=ord_prc,
        BnsTpCode=bns_tp_code,
        OrdprcPtnCode=ordprc_ptn_code
    )
    return CSPAT00601_Request(CSPAT00601InBlock1=in_block)