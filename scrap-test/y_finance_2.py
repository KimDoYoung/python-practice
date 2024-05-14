import yfinance as yf

# 주식 티커(symbol) 설정 (예: 애플 주식)
ticker = "AAPL"

# yfinance를 이용해 데이터 다운로드
stock_data = yf.download(ticker, start="2023-01-01", end="2023-12-31")

# 데이터 확인
print(stock_data.head())

# Ticker 객체 생성
apple = yf.Ticker("AAPL")

# 현재 주식 가격 정보
current_price = apple.history(period="1d")
print(current_price)