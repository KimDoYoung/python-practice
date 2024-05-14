import yfinance as yf

# 삼성전자 티커(symbol) 설정
ticker = "005930.KS"

# yfinance를 이용해 데이터 다운로드
stock_data = yf.download(ticker, start="2023-01-01", end="2023-12-31")

# 데이터 확인
print(stock_data.head())

# 종가(Close) 데이터 시각화
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 5))
plt.plot(stock_data['Close'], label='Close Price')
plt.title(f'{ticker} 주식 종가')
plt.xlabel('Date')
plt.ylabel('Close Price (KRW)')
plt.legend()
plt.show()