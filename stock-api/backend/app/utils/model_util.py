from backend.app.domains.stc.common_model import CancelOrder_Request, ModifyOrder_Request, Order_Request
from backend.app.domains.stc.ls.model.cspat00601_model import CSPAT00601_Request, CSPAT00601InBlock1
from backend.app.domains.stc.ls.model.cspat00701_model import CSPAT00701_Request, CSPAT00701InBlock1
from backend.app.domains.stc.ls.model.cspat00801_model import CSPAT00801_Request, CSPAT00801InBlock1


def order_to_cspat00601_Request(order: Order_Request) -> CSPAT00601_Request:
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

def modify_order_to_cspat00701_Request(order: ModifyOrder_Request)-> CSPAT00701_Request:
    ordprc_ptn_code = '00' if order.cost > 0 else '03'
    
    in_block = CSPAT00701InBlock1(
        OrgOrdNo=order.org_ord_no,
        IsuNo=order.stk_code,
        OrdQty=order.qty,
        OrdprcPtnCode=ordprc_ptn_code,
        OrdPrc=float(order.cost),
        OrdCndiTpCode="0"
    )
    
    return CSPAT00701_Request(CSPAT00701InBlock1=in_block)    

def cancel_order_to_cspat00801_Request(order: CancelOrder_Request)-> CSPAT00801_Request:
    in_block = CSPAT00801InBlock1(
        OrgOrdNo=order.org_order_no,
        IsuNo=order.stk_code,
        OrdQty=order.qty,
    )
    
    return CSPAT00801_Request(CSPAT00801InBlock1=in_block)