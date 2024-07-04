from datetime import datetime


def get_today():
    ''' 오늘 날짜를 반환한다. '''
    yoils = ["월", "화", "수", "목", "금", "토", "일"]
    yoil = datetime.now().weekday()
    yoil_korean = yoils[yoil]
    today = datetime.now().strftime("%Y-%m-%d")
    today = f"{today} ({yoil_korean})"
    return today
