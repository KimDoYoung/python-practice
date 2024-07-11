# ls_websocket_model.py
"""
모듈 설명: 
    - LS증권 웹소켓으로 받는 데이터 모델들
주요 기능:
    -   기능을 넣으시오

작성자: 김도영
작성일: 2024-07-11
버전: 1.0
"""
from typing import Optional
from pydantic import BaseModel


class Header(BaseModel):
    tr_cd: str
    tr_key: Optional[str] = None

class NewsBody(BaseModel):
    date: str
    code: str
    realkey: str
    bodysize: str
    time: str
    id: str
    title: str

from pydantic import BaseModel

class Sc0Body(BaseModel):
    ''' 주식주문접수 '''
    lineseq: str # 라인일련번호
    accno: str # Push키
    user: str # 조작자ID
    len: str # 헤더길이
    gubun: str # 헤더구분
    compress: str # 압축구분
    encrypt: str # 암호구분
    offset: str # 공통시작지점
    trcode: str # TRCODE SONAT000:신규주문 SONAT001:정정주문 SONAT002:취소주문 SONAS100:체결확인
    compid: str # 이용사번호
    userid: str # 사용자ID
    media: str # 접속매체
    ifid: str # I/F일련번호
    seq: str # 전문일련번호
    trid: str # TR추적ID
    pubip: str # 공인IP
    privip: str # 사설IP
    pcbpno: str # 처리지점번호
    bpno: str # 지점번호
    termno: str # 단말번호
    lang: str # 언어구분
    proctm: str # AP처리시간
    msgcode: str # 메세지코드
    outgu: str # 메세지출력구분
    compreq: str # 압축요청구분
    funckey: str # 기능키
    reqcnt: str # 요청레코드개수
    filler: str # 예비영역
    cont: str # 연속구분
    contkey: str # 연속키값
    varlen: str # 가변시스템길이
    varhdlen: str # 가변해더길이
    varmsglen: str # 가변메시지길이
    trsrc: str # 조회발원지
    eventid: str # I/F이벤트ID
    ifinfo: str # I/F정보
    filler1: str # 예비영역
    ordchegb: str # 주문체결구분 01:주문 02:정정 03:취소 11:체결 12:정정확인 13:취소확인 14:거부 A1:접수중 AC:접수완료
    marketgb: str # 시장구분 00:비상장 10:코스피 11:채권 19:장외시장 20:코스닥 23:코넥스 30:프리보드 61:동경거래소 62:JASDAQ
    ordgb: str # 주문구분 01:현금매도 02:현금매수 03:신용매도 04:신용매수 05:저축매도 06:저축매수 07:상품매도(대차) 09:상품매도 10:상품매수 11:선물대용매도(일반) 12:선물대용매도(반대) 13:현금매도(프) 14:현금매수(프) 15:현금매수(유가) 16:현금매수(정리) 17:상품매도(대차.프) 19:상품매도(프) 20:상품매수(프) 30:장외매매
    orgordno: str # 원주문번호
    accno1: str # 계좌번호
    accno2: str # 계좌번호
    passwd: str # 비밀번호
    expcode: str # 종목번호 표준코드 12자리
    shtcode: str # 단축종목번호 주식은 단축코드 앞에 A포함 7자리 ELW는 단축코드 앞에 J포함 7자리
    hname: str # 종목명
    ordqty: str # 주문수량
    ordprice: str # 주문가격
    hogagb: str # 주문조건 0:없음 1:IOC 2:FOK
    etfhogagb: str # 호가유형코드 00:지정가 03:시장가 05:조건부지정가 06:최유리지정가 07:최우선지정가 09:자사주 10:매입인도(일반) 13:시장가(IOC) 16:최유리지정가(IOC) 18:사용안함 20:지정가(임의) 23:시장가(임의) 26:최유리지정가(FOK) 41:부분충족(프리보드) 42:전량충족(프리보드) 51:장중대량 52:장중바스켓 61:장개시전시간외 62:사용안함 63:경매매 66:장전시간외경쟁대량 67:장개시전시간외대량 68:장개시전시간외바스켓 69:장개시전시간외자사주 71:신고대량전장시가 72:사용안함 73:신고대량종가 76:장중경쟁대량 77:장중대량 78:장중바스켓 79:사용안함 80:매입인도(당일) 81:시간외종가 82:시간외단일가 87:시간외대량 88:바스켓주문 89:시간외자사주 91:자사주스톡옵션 A1:stop order
    pgmtype: str # 프로그램호가구분 00:일반 01:지수차익 02:지수비차익 03:주식차익 04:ETF차익(비차익제외) 05:ETF설정(비차익제외) 06:ETF차익(비차익) 07:ETF설정(비차익) 08:DR차익 09:ELW LP헷지 10:ETF LP헷지 11:주식옵션 LP헷지 12:장외파생상품헷지
    gmhogagb: str # 공매도호가구분 0:일반 1:차입주식매도 2:기타공매도
    gmhogayn: str # 공매도가능여부 0:일반 1:공매도
    singb: str # 신용구분 000:보통 001:유통융자신규 003:자기융자신규 005:유통대주신규 007:자기대주신규 011:미사용 070:매도대금담보융자신규 080:예탁주식담보융자신규 082:예탁채권담보융자신규 101:유통융자상환 103:자기융자상환 105:유통대주상환 107:자기대주상환 111:유통융자전액상환 113:자기융자전액상환 170:매도대금담보융자상환 180:예탁주식담보융자상환 182:예탁채권담보융자상환 188:담보대출전액상환 201:유통융자현금상환 203:자기융자현금상환 205:유통대주현물상환 207:자기대주현물상환 280:예탁주식담보융자현금상환 282:예탁채권담보융자현금상환 301:유통융자현금상환취소 303:자기융자현금상환취소 305:유통대주현물상환취소 307:자기대주현물상환취소
    loandt: str # 대출일
    cvrgordtp: str # 반대매매주문구분 0:일반 1:자동반대매매 2:지점반대매매 3:예비주문에대한 본주문
    strtgcode: str # 전략코드
    groupid: str # 그룹ID
    ordseqno: str # 주문회차
    prtno: str # 포트폴리오번호
    basketno: str # 바스켓번호
    trchno: str # 트렌치번호
    itemno: str # 아아템번호
    brwmgmyn: str # 차입구분
    mbrno: str # 회원사번호
    procgb: str # 처리구분
    admbrchno: str # 관리지점번호
    futaccno: str # 선물계좌번호
    futmarketgb: str # 선물상품구분
    tongsingb: str # 통신매체구분
    lpgb: str # 유동성공급자구분 0:해당없음 1:유동성공급자
    dummy: str # DUMMY
    ordno: str # 주문번호
    ordtm: str # 주문시각
    prntordno: str # 모주문번호
    mgempno: str # 관리사원번호
    orgordundrqty: str # 원주문미체결수량
    orgordmdfyqty: str # 원주문정정수량
    ordordcancelqty: str # 원주문취소수량
    nmcpysndno: str # 비회원사송신번호
    ordamt: str # 주문금액
    bnstp: str # 매매구분 1:매도 2:매수
    spareordno: str # 예비주문번호
    cvrgseqno: str # 반대매매일련번호
    rsvordno: str # 예약주문번호
    mtordseqno: str # 복수주문일련번호
    spareordqty: str # 예비주문수량
    orduserid: str # 주문사원번호
    spotordqty: str # 실물주문수량
    ordruseqty: str # 재사용주문수량
    mnyordamt: str # 현금주문금액
    ordsubstamt: str # 주문대용금액
    ruseordamt: str # 재사용주문금액
    ordcmsnamt: str # 수수료주문금액
    crdtuseamt: str # 사용신용담보재사용금
    secbalqty: str # 잔고수량 실서버 데이터 미제공 필드
    spotordableqty: str # 실물가능수량 실서버 데이터 미제공 필드
    ordableruseqty: str # 재사용가능수량(매도) 실서버 데이터 미제공 필드
    flctqty: str # 변동수량
    secbalqtyd2: str # 잔고수량(D2) 실서버 데이터 미제공 필드
    sellableqty: str # 매도주문가능수량 실서버 데이터 미제공 필드
    unercsellordqty: str # 미체결매도주문수량 실서버 데이터 미제공 필드
    avrpchsprc: str # 평균매입가 실서버 데이터 미제공 필드
    pchsamt: str # 매입금액 실서버 데이터 미제공 필드
    deposit: str # 예수금
    substamt: str # 대용금
    csgnmnymgn: str # 위탁증거금현금
    csgnsubstmgn: str # 위탁증거금대용
    crdtpldgruseamt: str # 신용담보재사용금
    ordablemny: str # 주문가능현금
    ordablesubstamt: str # 주문가능대용
    ruseableamt: str # 재사용가능금액

class Sc1Body(BaseModel):
    ''' 주식주문체결 '''
    grpId: str # 그룹Id
    trchno: str # 트렌치번호
    trtzxLevytp: str # 거래세징수구분
    ordtrxptncode: str # 주문처리유형코드
    acntnm: str # 계좌명
    trcode: str # TRCODE SONAT000:신규주문 SONAT001:정정주문 SONAT002:취소주문 SONAS100:체결확인
    userid: str # 사용자ID
    agrgbrnno: str # 집계지점번호
    regmktcode: str # 등록시장코드
    len: str # 헤더길이
    opdrtnno: str # 운용지시번호
    orgordmdfyqty: str # 원주문정정수량
    avrpchsprc: str # 평균매입가
    exectime: str # 체결시각
    cont: str # 연속구분
    mnymgnrat: str # 현금증거금률
    mdfycnfqty: str # 정정확인수량
    orgordcancqty: str # 원주문취소수량
    compress: str # 압축구분
    execprc: str # 체결가격
    mdfycnfprc: str # 정정확인가격
    unercsellordqty: str # 미체결매도주문수량
    cmsnamtexecamt: str # 수수료체결금액
    ruseableamt: str # 재사용가능금액
    gubun: str # 헤더구분
    trid: str # TR추적ID
    flctqty: str # 변동수량
    execno: str # 체결번호
    lptp: str # 유동성공급자구분
    varmsglen: str # 가변메시지길이
    ordno: str # 주문번호
    futsmkttp: str # 선물시장구분
    crdtexecamt: str # 신용체결금액
    deposit: str # 예수금
    frgrunqno: str # 외국인고유번호
    crdayruseexecval: str # 금일재사용체결금액
    trsrc: str # 조회발원지
    ordacntno: str # 주문계좌번호
    reqcnt: str # 요청레코드개수
    shtnIsuno: str # 단축종목번호
    accno1: str # 계좌번호
    strtgcode: str # 전략코드
    ordseqno: str # 주문회차
    Isunm: str # 종목명
    ordablesubstamt: str # 주문가능대용
    encrypt: str # 암호구분
    Isuno: str # 종목번호
    accno2: str # 계좌번호
    contkey: str # 연속키값
    Loandt: str # 대출일
    seq: str # 전문일련번호
    lineseq: str # 라인일련번호
    varlen: str # 가변시스템길이
    orduserId: str # 주문자Id
    mgmtbrnno: str # 관리지점번호
    rjtqty: str # 거부수량
    ordprcptncode: str # 호가유형코드 00:지정가 03:시장가 05:조건부지정가 06:최유리지정가 07:최우선지정가 09:자사주 10:매입인도(일반) 13:시장가 (IOC) 16:최유리지정가 (IOC) 18:사용안함 20:지정가(임의) 23:시장가(임의) 26:최유리지정가 (FOK) 41:부분충족(프리보드) 42:전량충족(프리보드) 51:장중대량 52:장중바스켓 61:장개시전시간외 62:사용안함 63:경매매 66:장전시간외경쟁대량 67:장개시전시간외대량 68:장개시전시간외바스켓 69:장개시전시간외자사주 71:신고대량전장시가 72:사용안함 73:신고대량종가 76:장중경쟁대량 77:장중대량 78:장중바스켓 79:사용안함 80:매입인도(당일) 81:시간외종가 82:시간외단일가 87:시간외대량 88:바스켓주문 89:시간외자사주 91:자사주스톡옵션 A1:stop order
    stdIsuno: str # 표준종목번호
    pchsant: str # 매입금액
    filler: str # 예비영역
    secbalqty: str # 잔고수량
    ordxctptncode: str # 주문체결유형코드 01:주문 02:정정 03:취소 11:체결 12 정정확인 13 취소확인 14 거부
    canccnfqty: str # 취소확인수량
    ordablemny: str # 주문가능현금
    pubip: str # 공인IP
    prvip: str # 사설IP
    funckey: str # 기능키
    accno: str # 계좌번호
    compreq: str # 압축요청구분
    crdtpldgruseamt: str # 신용담보재사용금
    ordamt: str # 주문금액
    termno: str # 단말번호
    crdtpldgexecamt: str # 신용담보체결금액
    ordcndi: str # 주문조건
    rmndLoanamt: str # 잔여대출금액
    bpno: str # 지점번호
    substamt: str # 대용금
    mgempno: str # 관리사원번호
    csgnsubstmgn: str # 위탁증거금대용
    offset: str # 공통시작지점
    rcptexectime: str # 거래소수신체결시각
    sellableqty: str # 매도주문가능수량
    spotexecqty: str # 실물체결수량
    varhdlen: str # 가변해더길이
    substmgnrat: str # 대용증거금률
    ordavrexecprc: str # 주문평균체결가격
    itemno: str # 아이템번호
    mgntrncode: str # 신용거래코드 [신규] 000 : 보통 001 : 유통융자신규 003 : 자기융자신규 005 : 유통대주신규 007 : 자기대주신규 080 : 예탁주식담보융자신규 082 : 예탁채권담보융자신규 [상환] 101 : 유통융자상환 103 : 자기융자상환 105 : 유통대주상환 107 : 자기대주상환 111 : 유통융자전액상환 113 : 자기융자전액상환 180 : 예탁주식담보융자상환 182 : 예탁채권담보융자상환 188 : 담보대출전액상환
    nsavtrdqty: str # 비저축체결수량
    ifinfo: str # I/F정보
    ordableruseqty: str # 재사용가능수량(매도)
    ptflno: str # 포트폴리오번호
    secbalqtyd2: str # 잔고수량(d2)
    brwmgmtYn: str # 차입관리여부
    eventid: str # I/F이벤트ID
    csgnmnymgn: str # 위탁증거금현금
    pcbpno: str # 처리지점번호
    orgordno: str # 원주문번호
    ifid: str # I/F일련번호
    media: str # 접속매체
    mtiordseqno: str # 복수주문일련번호
    filler1: str # 예비영역
    orgordunercqty: str # 원주문미체결수량
    mbrnmbrno: str # 회원/비회원사번호
    futsLnkbrnno: str # 선물연계지점번호
    commdacode: str # 통신매체코드
    stslexecqty: str # 공매도체결수량
    proctm: str # AP처리시간
    bfstdIsuno: str # 전표준종목번호
    futsLnkacntno: str # 선물연계계좌번호
    lang: str # 언어구분
    unercqty: str # 미체결수량(주문)
    execqty: str # 체결수량
    adduptp: str # 수수료합산코드
    bskno: str # 바스켓번호
    spotordableqty: str # 실물가능수량
    ubstexecamt: str # 대용체결금액
    cvrgordtp: str # 반대매매주문구분 0:일반 1:자동반대매매 2:지점반대매매 3:예비주문에대한 본주문
    ordqty: str # 주문수량
    mnyexecamt: str # 현금체결금액
    outgu: str # 메세지출력구분
    msgcode: str # 메세지코드
    ordtrdptncode: str # 주문거래유형코드 00: 위탁 01: 신용 04: 선물대용
    ordmktcode: str # 주문시장코드
    ordptncode: str # 주문유형코드 00 해당없음 01:현금매도 02:현금매수 03신용매도 04:신용매수
    prdayruseexecval: str # 전일재사용체결금액
    comid: str # COM ID
    bnstp: str # 매매구분 1:매도 2:매수
    user: str # 조작자ID
    ordprc: str # 주문가격

class LsWsResponse(BaseModel):
    header: Header

class NewsResponse(LsWsResponse):
    body: NewsBody

# 주식주문접수
class Sc0Response(LsWsResponse):
    body: Sc0Body
    
# 주식주문체결
class Sc1Response(LsWsResponse):
    body: Sc1Body
    
    def data_for_client_ws(self) -> dict:
        return {
            "exectime" : self.body.exectime,
            
        }

# 주식주문정정
class Sc2Response(LsWsResponse):
    body: Sc1Body

# 주식 주문취소
class Sc3Response(LsWsResponse):
    body: Sc1Body
