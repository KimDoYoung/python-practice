from datetime import datetime


def test1(msg: str):
    print("스케줄테스트 " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " : " + msg)
    return 1
