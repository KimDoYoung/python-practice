#  websocket-client 라이브러리를 사용하는 것은 권장되지 않습니다. 
# 대신, 비동기 웹소켓 라이브러리를 사용하는 것이 더 적합합니다. 
# websockets 라이브러리와 같은 비동기 웹소켓 클라이언트를 사용할 수 있습니다.
import websocket
from backend.app.core.logger import get_logger

logger = get_logger(__name__)


def on_open(ws):
    logger.info("웹소켓 연결이 열렸습니다.")

def on_message(ws, message):
    logger.info(f"웹소켓으로부터 받은 데이터: {message}")

def on_error(ws, error):
    logger.error(f"웹소켓 에러 발생: {error}")

def on_close(ws):
    logger.info("웹소켓 연결이 닫혔습니다.")

def main():
    # 웹소켓 연결 생성 및 실행
    ws = websocket.WebSocketApp("ws://ops.koreainvestment.com:21000",
                                on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)

    # 웹소켓을 비동기로 실행
    ws.run_forever()


if __name__ == "__main__":
    main()