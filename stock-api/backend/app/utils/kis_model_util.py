# kis_model_util.py
"""
모듈 설명: 
    - KIS interface model -> api model로 변경하는 유틸리티
주요 기능:

작성자: 김도영
작성일: 2024-07-14
버전: 1.0
"""

from backend.app.domains.stc.kis.model.kis_inquire_daily_ccld_model import InquireDailyCcld_Request
from backend.app.domains.stc.kis.model.kis_inquire_psble_order import InquirePsblOrder_Request
from backend.app.domains.stc.kis.model.kis_order_cash_model import KisOrderRvsecncl_Request
from backend.app.domains.stc.kis_interface_model import Buy_Max_Request, DailyCcld_Request, Modify_Order_Request
from backend.app.utils.misc_util import only_number


def daily_ccld_to_inquire_daily_ccld(daily_ccld: DailyCcld_Request ) -> InquireDailyCcld_Request :
    ''' 주식일별주문체결조회 DailyCcld_Request -> InquireDailyCcld_Request '''
    start_ymd = only_number(daily_ccld.start_ymd)
    end_ymd = only_number(daily_ccld.end_ymd)
    return InquireDailyCcld_Request(
        inqr_strt_dt=start_ymd,
        inqr_end_dt=end_ymd
    )

def modify_order_to_kisOrderRvsecncl_request(user_req: Modify_Order_Request) -> KisOrderRvsecncl_Request:
    # 주문구분 설정
    if user_req.modify_cost == "0":
        order_division = "01"  # 시장가
    else:
        order_division = "00"  # 지정가

    # 정정/취소 구분 코드 설정
    if user_req.dvsn_cd == "정정":
        rvse_cncl_division_code = "01"
    else:
        rvse_cncl_division_code = "02"

    return KisOrderRvsecncl_Request(
        ORGN_ODNO=user_req.order_no,
        ORD_DVSN=order_division,
        RVSE_CNCL_DVSN_CD=rvse_cncl_division_code,
        ORD_QTY=user_req.modify_qty,
        ORD_UNPR=user_req.modify_cost,
        QTY_ALL_ORD_YN=user_req.all_yn
    )

def buy_max_to_InquirePsblOrder_Request(user_req: Buy_Max_Request) -> InquirePsblOrder_Request:
    if user_req.cost == "0":
        ord_dvsn = '01'
    else:
        ord_dvsn = '00'
    return InquirePsblOrder_Request(
        pdno=user_req.stk_code,
        ord_unpr=user_req.cost,
        ord_dvsn=ord_dvsn
    )