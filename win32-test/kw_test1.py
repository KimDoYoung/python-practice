import pprint
from pykiwoom.kiwoom import *

kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)
print("블록킹 로그인 완료")

account_num = kiwoom.GetLoginInfo("ACCOUNT_CNT")        # 전체 계좌수
accounts = kiwoom.GetLoginInfo("ACCNO")                 # 전체 계좌 리스트
user_id = kiwoom.GetLoginInfo("USER_ID")                # 사용자 ID
user_name = kiwoom.GetLoginInfo("USER_NAME")            # 사용자명
keyboard = kiwoom.GetLoginInfo("KEY_BSECGB")            # 키보드보안 해지여부
firewall = kiwoom.GetLoginInfo("FIREW_SECGB")           # 방화벽 설정 여부

print(f"전체계좌수:{account_num}")
print(f"전체계좌:{accounts}")
print("사용자 ID" + user_id)
print("사용자명 " + user_name)

note = "키보드보안 해지여부: "
if keyboard == "0":
    print("{note}정상")
elif keyboard == "1":
    print("{note}해지")
else:
    print("{note}알 수 없음")
note = "방화벽 설정 여부:"
if firewall == "0":
    print(f"{note}미설정")
elif firewall == "1":
    print(f"{note}설정")
elif firewall == "2":
    print(f"{note}해지")
else:
    print(f"{note}알 수 없음")

market_code_dict = {
    "0": "코스피",
    "3": "ELW",
    "4": "뮤추얼펀드",
    "5": "신주인수권",
    "6": "리츠",
    "8": "ETF",
    "9": "하이얼펀드",
    "10": "코스닥",
    "30": "K-OTC",
    "50": "코넥스"
}

# 종목코드얻기

# kospi = kiwoom.GetCodeListByMarket('0')
# kosdaq = kiwoom.GetCodeListByMarket('10')
# etf = kiwoom.GetCodeListByMarket('8')

# print(len(kospi), kospi)
# print(len(kosdaq), kosdaq)
# print(len(etf), etf)
# 000020
#종목명
code = "000020"
name = kiwoom.GetMasterCodeName(code)
print(name)

state = kiwoom.GetConnectState()
if state == 0:
    print("미연결")
elif state == 1:
    print("연결완료")

stock_cnt = kiwoom.GetMasterListedStockCnt("005930")
print("삼성전자 상장주식수: ", stock_cnt)

stock_cnt = kiwoom.GetMasterListedStockCnt(code)
print(f"{name} 상장주식수: ", stock_cnt)

#  '정상', '투자주의', '투자경고', '투자위험', '투자주의환기종목'의 값을 갖습니다.
gamri_gubun = kiwoom.GetMasterConstruction(code)
print(f"{name}의 감리구분: {gamri_gubun}")

# 상장일
opendate = kiwoom.GetMasterListedStockDate(code)
print(opendate)
print(type(opendate))        # datetime.datetime 객체

# 전일가?
전일가 = kiwoom.GetMasterLastPrice(code)
print(f"{name} 전일가 : {int(전일가)}")
print(type(전일가))

종목상태 = kiwoom.GetMasterStockState(code)
print(종목상태)

