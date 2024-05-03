import time
from pykiwoom.kiwoom import *

kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)
# try:
#     df = kiwoom.block_request("opt10001",
#                             종목코드="005930",
#                             output="주식기본정보",
#                             next=0)
#     print(df)   
# except Exception as e:
#     print(e)

# kiwoom = Kiwoom()
# kiwoom.CommConnect(block=True)

# TR 요청 (연속조회)
dfs = []
df = kiwoom.block_request("opt10081",
                          종목코드="005930",
                          기준일자="20240503",
                          수정주가구분=1,
                          output="주식일봉차트조회",
                          next=0)
print(df.head())
dfs.append(df)

while kiwoom.tr_remained:
    df = kiwoom.block_request("opt10081",
                              종목코드="005930",
                              기준일자="20240503",
                              수정주가구분=1,
                              output="주식일봉차트조회",
                              next=2)
    dfs.append(df)
    time.sleep(1)

df = pd.concat(dfs)
df.to_excel("data\\005930.xlsx")