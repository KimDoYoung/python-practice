from backend.app.domains.stc.ls.model.t1441_model import T1441INBLOCK, T1441_Request
from backend.app.domains.stc.ls.model.t1452_model import T1452INBLOCK, T1452_Request
from backend.app.domains.stc.ls.model.t1466_model import T1466INBLOCK, T1466_Request
from backend.app.domains.stc.ls.model.t1481_model import T1481INBLOCK, T1481_Request
from backend.app.domains.stc.ls.model.t1482_model import T1482INBLOCK, T1482_Request
from backend.app.domains.stc.ls.model.t1489_model import T1489INBLOCK, T1489_Request
from backend.app.domains.stc.ls.model.t1492_model import T1492INBLOCK, T1492_Request
from backend.app.domains.stc.ls_interface_model import AcctHistory_Request, CancelOrder_Request, Fulfill_Api_Request, Fulfill_Request, HighItem_Request, ModifyOrder_Request, Order_Request
from backend.app.domains.stc.ls.model.cdpcq04700_model import CDPCQ04700_Request, CDPCQ04700InBlock1
from backend.app.domains.stc.ls.model.cspaq13700_model import CSPAQ13700_Request, CSPAQ13700InBlock1_Item
from backend.app.domains.stc.ls.model.cspat00601_model import CSPAT00601_Request, CSPAT00601InBlock1
from backend.app.domains.stc.ls.model.cspat00701_model import CSPAT00701_Request, CSPAT00701InBlock1
from backend.app.domains.stc.ls.model.cspat00801_model import CSPAT00801_Request, CSPAT00801InBlock1
from backend.app.domains.stc.ls.model.t0425_model import T0425INBLOCK, T0425_Request


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
    '''LS 현물정정주문 요청 모델로 변환'''
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
    '''LS 현물주문취소 요청 모델로 변환'''
    in_block = CSPAT00801InBlock1(
        OrgOrdNo = order.org_ord_no,
        IsuNo = order.stk_code,
        OrdQty = order.qty
    )
    
    return CSPAT00801_Request(CSPAT00801InBlock1=in_block)

def acct_history_to_CDPCQ04700_Request(acct_request: AcctHistory_Request) -> CDPCQ04700_Request:
    ''' LS 계좌별 거래내역 조회 요청 모델로 변환'''
    in_block = CDPCQ04700InBlock1(
        QrySrtDt=acct_request.from_ymd,
        QryEndDt=acct_request.to_ymd,
        SrtNo=acct_request.start_no,
        IsuNo=acct_request.stk_code
    )
    
    cdpcq_request = CDPCQ04700_Request(
        CDPCQ04700InBlock1=in_block
    )
    
    return cdpcq_request

def fulfill_to_t0425_Request(fulfill_request: Fulfill_Request) -> T0425_Request:
    # fullfill_type 매핑
    chegb_mapping = {
        '전체': '0',
        '체결': '1',
        '미체결': '2'
    }
    
    # buy_sell_gb 매핑
    medosu_mapping = {
        '전체': '0',
        '매수': '1',
        '매도': '2'
    }

    t0425InBlock = T0425INBLOCK(
        expcode=fulfill_request.stk_code,
        chegb=chegb_mapping[fulfill_request.fullfill_type],
        medosu=medosu_mapping[fulfill_request.buy_sell_gb]
    )

    t0425_request = T0425_Request(
        t0425InBlock=t0425InBlock
    )

    return t0425_request

def fulfill_api_to_cspaq13700_Request(req: Fulfill_Api_Request) -> CSPAQ13700_Request:
    # market_gb 매핑
    market_gb_map = {
        '전체': '00',
        '거래소': '10',
        '코스닥': '20',
        '프리보드': '30'
    }
    ord_mkt_code = market_gb_map[req.market_gb]

    # buy_sell_gb 매핑
    buy_sell_gb_map = {
        '전체': '0',
        '매도': '1',
        '매수': '2'
    }
    bns_tp_code = buy_sell_gb_map[req.buy_sell_gb]

    # fullfill_type 매핑
    fullfill_type_map = {
        '전체': '0',
        '체결': '1',
        '미체결': '3'
    }
    exec_yn = fullfill_type_map[req.fullfill_type]

    # ord_ptn_code 매핑
    ord_ptn_code_map = {
        '전체': '00',
        '매도전체': '98',
        '매수전체': '99',
        '현금매도': '01',
        '현금매수': '02',
        '저축매도': '05',
        '저축매수': '06',
        '상품매도': '09',
        '상품매수': '10',
        '융자매도': '03',
        '융자매수': '04',
        '대주매도': '07',
        '대주매수': '08',
        '선물대용매도': '11',
        '현금매도(프)': '13',
        '현금매수(프)': '14',
        '대출': '17',
        '대출상환': '18'
    }
    ord_ptn_code = ord_ptn_code_map[req.ord_ptn_code]

    if req.stk_code:
        IsuNo = 'A'+ req.stk_code 
    else:
        IsuNo = ''

    in_block = CSPAQ13700InBlock1_Item(
        OrdMktCode=ord_mkt_code,
        BnsTpCode=bns_tp_code,
        IsuNo=IsuNo,
        ExecYn=exec_yn,
        OrdDt=req.order_dt,
        OrdPtnCode=ord_ptn_code
    )

    return CSPAQ13700_Request(CSPAQ13700InBlock1=in_block)

#--------------------------------------------------------------------------------------
# 상위랭크 route
#--------------------------------------------------------------------------------------
def high_item_to_T1441_Request(req: HighItem_Request) -> T1441_Request:
    ''' 등락율 상위 '''
    # gubun1 변환
    market_gb_map = {
        '전체': '0',
        '코스피': '1',
        '코스닥': '2'
    }
    gubun1 = market_gb_map[req.market_gb]

    # gubun2 변환
    updown_gb_map = {
        '상승': '0',
        '하락': '1',
        '보합': '2'
    }
    gubun2 = updown_gb_map[req.updown_gb]

    # gubun3 변환
    yester_or_today_map = {
        '금일': '0',
        '전일': '1'
    }
    gubun3 = yester_or_today_map[req.yester_or_today]

    # T1441INBLOCK 객체 생성
    t1441InBlock = T1441INBLOCK(
        gubun1=gubun1,
        gubun2=gubun2,
        gubun3=gubun3,
        jc_num=0x00400000 | 0x00800000 | 0x00200000 | 0x00000080 |0x00000100 | 0x00000200 | 0x00004000 | 0x04000000 | 0x01000000 | 0x80000000,
        sprice=0,
        eprice=0,
        volume=0,
        idx=req.idx,
        jc_num2=0
    )

    # T1441_Request 객체 생성 및 반환
    t1441_req = T1441_Request(
        t1441InBlock=t1441InBlock
    )

    return t1441_req

def high_item_to_T1452_Request(req: HighItem_Request) -> T1452_Request:
    ''' 거래량 상위 '''
    market_gb_map = {
        '전체': '0',
        '코스피': '1',
        '코스닥': '2'
    }
    gubun = market_gb_map[req.market_gb]

    # jnilgubun 변환
    yester_or_today_map = {
        '금일': '1',
        '전일': '2'
    }
    jnilgubun = yester_or_today_map[req.yester_or_today]

    # 상승/하락/보합은 sdiff와 ediff로 설정
    # updown_gb_map = {
    #     '상승': (0, 100),  # 예: 상승률 0% 이상 100% 이하
    #     '하락': (-100, 0),  # 예: 하락률 -100% 이상 0% 이하
    #     '보합': (0, 0)  # 예: 보합 0% 이상 0% 이하
    # }
    # sdiff, ediff = updown_gb_map[req.updown_gb]
    sdiff = 0
    ediff = 0
    # T1452INBLOCK 객체 생성
    t1452InBlock = T1452INBLOCK(
        gubun=gubun,
        jnilgubun=jnilgubun,
        sdiff=sdiff,
        ediff=ediff,
        jc_num=0,
        sprice=0,
        eprice=0,
        volume=0,
        idx=0
    )

    # T1452_Request 객체 생성 및 반환
    t1452_req = T1452_Request(
        t1452InBlock=t1452InBlock
    )

    return t1452_req

def high_item_to_T1466_Request(req: HighItem_Request) -> T1466_Request:
    ''' 전일동시간대비거래급증 '''
    market_gb_mapping = {
        '전체': '0',
        '코스피': '1',
        '코스닥': '2'
    }

    # 기본값 설정 (예시: 구체적인 규칙이 제공되지 않았기 때문에 가정함)
    default_jc_num = 0
    default_jc_num2 = 0
    default_sprice = 0
    default_eprice = 0
    default_volume = 0
    default_idx = 0
    default_type1 = '0'
    default_type2 = '0'

    # 매핑 적용
    t1466InBlock = T1466INBLOCK(
        gubun=market_gb_mapping.get(req.market_gb, '0'),
        type1=default_type1,
        type2=default_type2,
        jc_num=default_jc_num,
        sprice=default_sprice,
        eprice=default_eprice,
        volume=default_volume,
        idx=default_idx,
        jc_num2=default_jc_num2
    )

    return T1466_Request(t1466InBlock=t1466InBlock)

def high_item_to_T1481_Request(req: HighItem_Request) -> T1481_Request:
    ''' 시간외등락율상위'''
    market_map = {
        '전체': '0',
        '코스피': '1',
        '코스닥': '2'
    }
    gubun1 = market_map[req.market_gb]
    
    # updown_gb 매핑
    updown_map = {
        '상승': '0',
        '하락': '1',
        '보합': '0'  # 보합은 상승률로 처리
    }
    gubun2 = updown_map[req.updown_gb]
    
    # jongchk 및 volume 설정 (기본값으로 설정)
    jongchk = '0'
    volume = '0'
    
    # T1481INBLOCK 객체 생성
    t1481InBlock = T1481INBLOCK(
        gubun1=gubun1,
        gubun2=gubun2,
        jongchk=jongchk,
        volume=volume,
        idx=0
    )
    
    # T1481_Request 객체 생성 및 반환
    t1481_req = T1481_Request(
        tr_cont='N',
        tr_cont_key='',
        mac_address='',
        t1481InBlock=t1481InBlock
    )
    
    return t1481_req


def high_item_to_T1482_Request(req: HighItem_Request) -> T1482_Request:
    ''' 시간외거래량상위 '''
    market_map = {
        '전체': '0',
        '코스피': '1',
        '코스닥': '2'
    }
    gubun = market_map[req.market_gb]
    
    # jongchk 및 idx 설정 (기본값으로 설정)
    jongchk = '0'
    
    # T1482INBLOCK 객체 생성
    t1482InBlock = T1482INBLOCK(
        gubun=gubun,
        jongchk=jongchk,
        idx=0
    )
    
    # T1482_Request 객체 생성 및 반환
    t1482_req = T1482_Request(
        tr_cont='N',
        tr_cont_key='',
        mac_address='',
        t1482InBlock=t1482InBlock
    )
    
    return t1482_req

def high_item_to_T1489_Request(req: HighItem_Request) -> T1489_Request:
    ''' 예상체결량상위조회 '''
    market_map = {
        '전체': '0',
        '코스피': '1',
        '코스닥': '2'
    }
    gubun = market_map[req.market_gb]
    
    # jgubun 매핑
    jgubun_map = {
        '전일': '0',
        '금일': '1'
    }
    jgubun = jgubun_map[req.yester_or_today]
    
    # jongchk 및 기타 설정 (기본값으로 설정)
    jongchk = '0x00000000'  # 기본값 설정
    idx = 0
    yesprice = 0
    yeeprice = 0
    yevolume = 0
    
    # T1489INBLOCK 객체 생성
    t1489InBlock = T1489INBLOCK(
        gubun=gubun,
        jgubun=jgubun,
        jongchk=jongchk,
        idx=idx,
        yesprice=yesprice,
        yeeprice=yeeprice,
        yevolume=yevolume
    )
    
    # T1489_Request 객체 생성 및 반환
    t1489_req = T1489_Request(
        tr_cont='N',
        tr_cont_key='',
        mac_address='',
        t1489InBlock=t1489InBlock
    )
    
    return t1489_req


def high_item_to_T1492_Request(req: HighItem_Request) -> T1492_Request:
    ''' 단일가예상등락율상위'''
    market_map = {
        '전체': '0',
        '코스피': '1',
        '코스닥': '2'
    }
    gubun1 = market_map[req.market_gb]
    
    # updown_gb 매핑
    updown_map = {
        '상승': '0',
        '하락': '1',
        '보합': '0'  # 보합은 상승률로 처리
    }
    gubun2 = updown_map[req.updown_gb]
    
    # jongchk 기본값 설정
    jongchk = '0'
    
    # volume 기본값 설정
    volume = '0'
    
    # T1492INBLOCK 객체 생성
    t1492InBlock = T1492INBLOCK(
        gubun1=gubun1,
        gubun2=gubun2,
        jongchk=jongchk,
        volume=volume,
        idx=0
    )
    
    # T1492_Request 객체 생성 및 반환
    t1492_req = T1492_Request(
        tr_cont='N',
        tr_cont_key='',
        mac_address='',
        t1492InBlock=t1492InBlock
    )
    
    return t1492_req
