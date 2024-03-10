# main.py
from chart_history import create_database, ChartHistory
from sqlalchemy.orm import sessionmaker

# 데이터베이스 엔진 생성
engine = create_database()

# 세션 설정
Session = sessionmaker(bind=engine)
session = Session()

# 새로운 차트 히스토리 객체 생성 및 데이터베이스에 추가
new_chart = ChartHistory(user_id="ExampleUser", chart_type="bar", json='{"key": "value"}', url="http://example.com")
session.add(new_chart)
session.commit()

# 세션 닫기
session.close()
