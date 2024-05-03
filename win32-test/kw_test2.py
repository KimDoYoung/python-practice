
from pykiwoom.kiwoom import *
import pprint

kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)
print("블록킹 로그인 완료")

# 테마 그룹
group = kiwoom.GetThemeGroupList(1)
pprint.pprint(group)

tickers = kiwoom.GetThemeGroupCode('173')
for ticker in tickers:
    name = kiwoom.GetMasterCodeName(ticker)
    print(ticker, name)